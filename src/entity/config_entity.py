from src.constants import training_pipeline
from datetime import datetime
import os


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE
        self.artifact_name = training_pipeline.ARTIFACT_DIR_NAME
        self.artifact_dir = os.path.join(self.pipeline_name, self.artifact_name)



class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.movies_data_path = os.path.join(self.data_ingestion_dir, "movies.csv")
        self.credits_data_path = os.path.join(self.data_ingestion_dir, "credits.csv")
        self.final_data_path = os.path.join(self.data_ingestion_dir, training_pipeline.FINAL_DATA)


class DataProcessingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_processing_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_PROCESSING_DIR_NAME)
        self.final_df = os.path.join(self.data_processing_dir, "final_df.csv")


class RecommenderTrainingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.recommender_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.RECOMMENDER_DIR_NAME)
        self.vectorizer_path = os.path.join(self.recommender_dir, training_pipeline.RECOMMENDER_VECTORIZER_DIR_NAME)
        # Content-based cosine similarity matrix (current behaviour)
        self.similarity_matrix_content_path = os.path.join(
            self.recommender_dir,
            training_pipeline.RECOMMENDER_SIMILARITYMATRIX_CONTENT_DIR_NAME,
        )
        # Alternative similarity matrix (can be used for collaborative-style or hybrid scoring)
        self.similarity_matrix_alt_path = os.path.join(
            self.recommender_dir,
            training_pipeline.RECOMMENDER_SIMILARITYMATRIX_ALT_DIR_NAME,
        )

class RecommendationConfig:
    def __init__(self, num_recommendations=5):
        self.num_recommendations = num_recommendations