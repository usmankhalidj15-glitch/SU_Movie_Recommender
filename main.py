from src.logging.logger import logging
from src.exception_handling.exception import CustomException

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

from src.components.data_ingestion import Data_Ingestion
from src.components.data_preprocessing import DataProcessing
from src.components.recommender_training import RecommenderTraining
from src.components.recommend import RecommenderService
import sys


if __name__ == "__main__":
    try:
        logging.info("========== MOVIE RECOMMENDER PIPELINE STARTED ==========")

        # CONFIGS
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_processing_config = DataProcessingConfig(training_pipeline_config)
        recommender_training_config = RecommenderTrainingConfig(training_pipeline_config)
        recommendation_config = RecommendationConfig(num_recommendations=5)

        # DATA INGESTION
        ingestion = Data_Ingestion(data_ingestion_config)
        ingestion_artifacts = ingestion.initiate_data_ingestion()

        # DATA PROCESSING
        processing = DataProcessing(training_pipeline_config, ingestion_artifacts, data_processing_config)
        processing_artifacts = processing.initiate_processing()

        # MODEL RECOMMENDER TRAINING
        recommender_training = RecommenderTraining(training_pipeline_config, recommender_training_config, processing_artifacts)
        recommender_training_artifacts = recommender_training.initiate_recommendation_training()

        logging.info("========== PIPELINE FINISHED SUCCESSFULLY ==========")

        # RECOMMENDATION
        recommendation = RecommenderService(data_processing_artifacts=processing_artifacts, training_artifacts=recommender_training_artifacts, recommendation_config=recommendation_config)
        recommendation_artifacts = recommendation.recommend_movie("Batman")

        print(recommendation_artifacts)

        
        logging.info("End of project")

    except Exception as e:
        logging.info(CustomException(e, sys))
        raise CustomException(e, sys)
