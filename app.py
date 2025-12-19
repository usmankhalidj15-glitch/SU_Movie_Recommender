from flask import Flask, render_template, request
from src.utils.utils import fetch_posters_for_movies
from src.pipeline.training import TrainingPipeline
from src.components.recommend import RecommenderService
from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataProcessingConfig,
    RecommenderTrainingConfig,
    RecommendationConfig,
)
from src.entity.artifact_entity import DataProcessingArtifacts, RecomenderTrainingrArtifacts
import pandas as pd
import os


app = Flask(__name__)

NUM_DISPLAY_MOVIES = 10
POSTER_CACHE = {}  # simple in-memory cache to avoid repeated TMDB calls


def get_posters_cached(movie_list):
    """Fetch posters with a basic cache to speed up responses."""
    missing = [m for m in movie_list if m not in POSTER_CACHE]
    if missing:
        fetched = fetch_posters_for_movies(missing)
        POSTER_CACHE.update(fetched)
    return {m: POSTER_CACHE.get(m) for m in movie_list}

# --- Lightweight startup: reuse existing artifacts if they exist ---
training_pipeline_config = TrainingPipelineConfig()
data_processing_config = DataProcessingConfig(training_pipeline_config)
recommender_training_config = RecommenderTrainingConfig(training_pipeline_config)

artifacts_exist = all(
    [
        os.path.exists(data_processing_config.final_df),
        os.path.exists(recommender_training_config.vectorizer_path),
        os.path.exists(recommender_training_config.similarity_matrix_content_path),
        os.path.exists(recommender_training_config.similarity_matrix_alt_path),
    ]
)

if not artifacts_exist:
    # Run the heavy pipeline only once to create artifacts
    pipeline = TrainingPipeline()
    ingestion_artifact = pipeline.start_data_ingestion()
    processing_artifact = pipeline.start_data_processing(ingestion_artifact)
    training_artifact = pipeline.start_recommender_training(processing_artifact)
else:
    # Reuse already computed artifacts for fast startup
    processing_artifact = DataProcessingArtifacts(final_df=data_processing_config.final_df)
    training_artifact = RecomenderTrainingrArtifacts(
        vectorizer_path=recommender_training_config.vectorizer_path,
        similarity_matrix_content_path=recommender_training_config.similarity_matrix_content_path,
        similarity_matrix_alt_path=recommender_training_config.similarity_matrix_alt_path,
    )

df = pd.read_csv(processing_artifact.final_df)
all_movies = sorted(df["title"].tolist())

@app.route("/", methods=["GET"])
def home():
    sample_movies = all_movies[:NUM_DISPLAY_MOVIES]
    sample_posters = get_posters_cached(sample_movies)
    
    return render_template("index.html", 
                           movies=all_movies,
                           display_movies=sample_movies, 
                           movie_posters=sample_posters)

@app.route("/recommend", methods=["POST"])
def recommend():
    movie_name = request.form.get("movie")
    method = request.form.get("method", "content_cosine")

    try:
        config = RecommendationConfig(num_recommendations=5)

        service = RecommenderService(
            data_processing_artifacts=processing_artifact,
            training_artifacts=training_artifact,
            recommendation_config=config
        )

        result = service.recommend_movie(movie_name, method=method)
        recommended_movies = result.movies
        
        recommended_posters = get_posters_cached(recommended_movies)

        sample_movies = all_movies[:NUM_DISPLAY_MOVIES]
        sample_posters = get_posters_cached(sample_movies)
        
        return render_template(
            "index.html",
            movies=all_movies,
            display_movies=sample_movies,
            movie_posters=sample_posters,
            movie=movie_name,
            recommendations=recommended_movies,
            recommended_posters=recommended_posters,
            selected_method=method,
        )

    except Exception as e:
        sample_movies = all_movies[:NUM_DISPLAY_MOVIES]
        sample_posters = get_posters_cached(sample_movies)
        
        return render_template(
            "index.html",
            movies=all_movies,
            display_movies=sample_movies,
            movie_posters=sample_posters,
            error=str(e),
            selected_method=method,
        )

if __name__ == "__main__":
    app.run(debug=True)