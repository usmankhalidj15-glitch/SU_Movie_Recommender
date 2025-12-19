import sys
from src.logging.logger import logging
from src.exception_handling.exception import CustomException

from src.components.data_ingestion import Data_Ingestion
from src.components.data_preprocessing import DataProcessing
from src.components.recommender_training import RecommenderTraining
from src.components.recommend import RecommenderService

from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataProcessingConfig,
    RecommenderTrainingConfig,
    RecommendationConfig
)

from src.entity.artifact_entity import (
    DataIngestionArtifacts,
    DataProcessingArtifacts,
    RecomenderTrainingrArtifacts,
    RecoomendArtifacts
)


class TrainingPipeline:
    def __init__(self):
        try:
            logging.info("Initializing Training Pipeline configurations...")

            # ROOT PIPELINE CONFIG
            self.training_pipeline_config = TrainingPipelineConfig()

            # STAGE WISE CONFIGS
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            self.data_processing_config = DataProcessingConfig(self.training_pipeline_config)
            self.recommender_training_config = RecommenderTrainingConfig(self.training_pipeline_config)

            # RECOMMENDATION CONFIG
            self.recommendation_config = RecommendationConfig(num_recommendations=5)

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_ingestion(self):
        try:
            logging.info("==== Starting Data Ingestion ====")
            ingestion = Data_Ingestion(self.data_ingestion_config)
            return ingestion.initiate_data_ingestion()

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_processing(self, ingestion_artifact: DataIngestionArtifacts):
        try:
            logging.info("==== Starting Data Processing ====")
            process = DataProcessing(
                self.training_pipeline_config,
                ingestion_artifact,
                self.data_processing_config
            )
            return process.initiate_processing()

        except Exception as e:
            raise CustomException(e, sys)

    def start_recommender_training(self, processing_artifact: DataProcessingArtifacts):
        try:
            logging.info("==== Starting Recommender Training ====")
            trainer = RecommenderTraining(
                self.training_pipeline_config,
                self.recommender_training_config,
                processing_artifact
            )
            return trainer.initiate_recommendation_training()

        except Exception as e:
            raise CustomException(e, sys)

    def start_recommendation(self, processing_artifact, training_artifact):
        try:
            logging.info("==== Generating Movie Recommendations ====")

            service = RecommenderService(
                data_processing_artifacts=processing_artifact,
                training_artifacts=training_artifact,
                recommendation_config=self.recommendation_config
            )
            return service.recommend_movie("Batman")

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        try:
            logging.info("========== MOVIE RECOMMENDER PIPELINE STARTED ==========")

            # STAGE 1
            ingestion_artifact = self.start_data_ingestion()

            # STAGE 2
            processing_artifact = self.start_data_processing(ingestion_artifact)

            # STAGE 3
            recommender_training_artifact = self.start_recommender_training(processing_artifact)

            # STAGE 4 (optional)
            recommendation_artifact = self.start_recommendation(
                processing_artifact, recommender_training_artifact
            )

            logging.info("========== MOVIE RECOMMENDER PIPELINE FINISHED SUCCESSFULLY ==========")

            return recommendation_artifact

        except Exception as e:
            raise CustomException(e, sys)
