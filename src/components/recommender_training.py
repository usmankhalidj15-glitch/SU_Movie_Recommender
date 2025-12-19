from src.logging.logger import logging
from src.exception_handling.exception import CustomException
from src.constants import training_pipeline
from src.entity.artifact_entity import DataIngestionArtifacts, DataProcessingArtifacts, RecomenderTrainingrArtifacts
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataProcessingConfig, RecommenderTrainingConfig
import pandas as pd
import os, sys
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle

class RecommenderTraining:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig,
                 recommender_training_config: RecommenderTrainingConfig,
                 data_processing_artifacts: DataProcessingArtifacts):

        self.training_pipeline_config = training_pipeline_config
        self.recommender_training_config = recommender_training_config
        self.data_processing_artifacts = data_processing_artifacts
    def initiate_recommendation_training(self):
        try:
            logging.info("Reading the processed dataframe")
            df = pd.read_csv(self.data_processing_artifacts.final_df)

            logging.info("Vectorizing tags using CountVectorizer")
            cv = CountVectorizer(max_features=5000, stop_words="english")
            vectors = cv.fit_transform(df["tags"]).toarray()

            # --- METHOD 1: Content-based cosine similarity (existing behaviour) ---
            logging.info("Calculating content-based cosine similarity matrix")
            similarity_content = cosine_similarity(vectors)

            # --- METHOD 2: Alternative similarity (dot-product style) ---
            # This can be interpreted as an item-item collaborative style score in the
            # learned tag space. It gives higher scores to movies that share many strong tags.
            logging.info("Calculating alternative similarity matrix (dot-product on tag vectors)")
            similarity_alt = vectors @ vectors.T


            os.makedirs(self.recommender_training_config.recommender_dir, exist_ok=True)

            logging.info("Saving vectorizer.pkl")
            pickle.dump(cv, open(self.recommender_training_config.vectorizer_path, "wb"))

            # Save similarity matrices
            logging.info("Saving content similarity matrix")
            pickle.dump(
                similarity_content,
                open(self.recommender_training_config.similarity_matrix_content_path, "wb"),
            )

            logging.info("Saving alternative similarity matrix")
            pickle.dump(
                similarity_alt,
                open(self.recommender_training_config.similarity_matrix_alt_path, "wb"),
            )

            logging.info("=== MODEL TRAINING COMPLETED SUCCESSFULLY ===")

            # Return artifacts object
            return RecomenderTrainingrArtifacts(
                vectorizer_path=self.recommender_training_config.vectorizer_path,
                similarity_matrix_content_path=self.recommender_training_config.similarity_matrix_content_path,
                similarity_matrix_alt_path=self.recommender_training_config.similarity_matrix_alt_path,
            )
        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e, sys)