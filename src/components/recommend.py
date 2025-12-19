from src.logging.logger import logging
from src.exception_handling.exception import CustomException
from src.entity.config_entity import (
    DataIngestionConfig,
    DataProcessingConfig,
    TrainingPipelineConfig,
    RecommenderTrainingConfig,
    RecommendationConfig,
)
from src.entity.artifact_entity import (
    RecomenderTrainingrArtifacts,
    DataProcessingArtifacts,
    RecoomendArtifacts,
)
import pandas as pd
import os, sys
import pickle
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances


class RecommenderService:
    def __init__(
        self,
        data_processing_artifacts: DataProcessingArtifacts,
        training_artifacts: RecomenderTrainingrArtifacts,
        recommendation_config: RecommendationConfig,
    ):
        self.data_processing_artifacts = data_processing_artifacts
        self.training_artifacts = training_artifacts
        self.recommendation_config = recommendation_config
        self._vectors = None  # lazy-loaded tag vectors

    def _load_dataframe(self) -> pd.DataFrame:
        logging.info("Reading the dataframe")
        return pd.read_csv(self.data_processing_artifacts.final_df)

    def _get_movie_index(self, df: pd.DataFrame, movie: str) -> int:
        if movie not in df["title"].values:
            raise ValueError(f"{movie} not found in dataset.")
        return df[df["title"] == movie].index[0]

    def _get_recommendations_from_scores(
        self, df: pd.DataFrame, scores_row, movie_idx: int
    ) -> list:
        sim_scores = list(enumerate(scores_row))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Skip the movie itself at movie_idx
        sim_scores = [s for s in sim_scores if s[0] != movie_idx]
        sim_scores = sim_scores[: self.recommendation_config.num_recommendations]

        movie_indices = [i[0] for i in sim_scores]
        return df["title"].iloc[movie_indices].tolist()

    def _get_tag_vectors(self, df: pd.DataFrame):
        """
        Lazily load the trained CountVectorizer and transform the 'tags' column
        to get the same feature space as training. Reused for distance-based
        similarity methods.
        """
        if self._vectors is not None:
            return self._vectors

        logging.info("Loading vectorizer for distance-based similarity methods")
        with open(self.training_artifacts.vectorizer_path, "rb") as f:
            cv = pickle.load(f)

        self._vectors = cv.transform(df["tags"]).toarray()
        return self._vectors

    def recommend_movie(self, movie: str, method: str = "content_cosine") -> RecoomendArtifacts:
        try:
            df = self._load_dataframe()
            idx = self._get_movie_index(df, movie)

            # Choose which similarity / distance metric to use based on method
            if method == "content_cosine":
                logging.info("Loading content-based cosine similarity matrix")
                with open(self.training_artifacts.similarity_matrix_content_path, "rb") as f:
                    similarity_matrix = pickle.load(f)
                scores_row = similarity_matrix[idx]

            elif method == "collaborative_like":
                # Uses an alternative similarity matrix (dot-product style on tag vectors)
                logging.info("Loading collaborative-like similarity matrix")
                with open(self.training_artifacts.similarity_matrix_alt_path, "rb") as f:
                    similarity_matrix = pickle.load(f)
                scores_row = similarity_matrix[idx]

            elif method == "content_euclidean":
                logging.info("Using Euclidean distance on tag vectors")
                vectors = self._get_tag_vectors(df)
                # distances -> convert to similarity (smaller distance = higher similarity)
                dists = euclidean_distances(vectors[idx : idx + 1], vectors)[0]
                scores_row = -dists

            elif method == "content_manhattan":
                logging.info("Using Manhattan distance on tag vectors")
                vectors = self._get_tag_vectors(df)
                dists = manhattan_distances(vectors[idx : idx + 1], vectors)[0]
                scores_row = -dists

            elif method == "popularity":
                # Simple popularity-based fallback using vote_average and vote_count if present
                logging.info("Using popularity-based recommendation method")
                if "vote_average" in df.columns and "vote_count" in df.columns:
                    df["popularity_score"] = df["vote_average"] * df["vote_count"]
                    df_sorted = df.sort_values("popularity_score", ascending=False)
                    # Exclude the input movie from popularity list
                    df_sorted = df_sorted[df_sorted["title"] != movie]
                    recommendations = df_sorted["title"].head(self.recommendation_config.num_recommendations).tolist()
                else:
                    logging.info("vote_average/vote_count not in dataframe; falling back to content_cosine")
                    with open(self.training_artifacts.similarity_matrix_content_path, "rb") as f:
                        similarity_matrix = pickle.load(f)
                    scores_row = similarity_matrix[idx]
                    recommendations = self._get_recommendations_from_scores(df, scores_row, idx)

                logging.info(f"Popularity-based recommendations generated for '{movie}'")
                return RecoomendArtifacts(movies=recommendations)

            else:
                raise ValueError(f"Unknown recommendation method: {method}")

            # For similarity-matrix based methods:
            recommendations = self._get_recommendations_from_scores(df, scores_row, idx)

            logging.info(f"Recommendations generated for '{movie}' using method '{method}'")

            return RecoomendArtifacts(movies=recommendations)




        except Exception as e:
            logging.info(CustomException(e, sys))
            raise CustomException(e, sys)

