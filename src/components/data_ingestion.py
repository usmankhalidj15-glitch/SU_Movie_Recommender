import pandas as pd
import shutil, os,sys
from src.logging.logger import logging
from src.exception_handling.exception import CustomException
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifacts



class Data_Ingestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.info(CustomException(e, sys))
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self)->DataIngestionArtifacts:
        try:
            # make sure the director exists
            os.makedirs(self.data_ingestion_config.data_ingestion_dir, exist_ok=True)

            raw_movies_path = "data/raw/tmdb_5000_movies.csv"
            raw_credits_path = "data/raw/tmdb_5000_credits.csv"

            shutil.copy(raw_movies_path, self.data_ingestion_config.movies_data_path)
            shutil.copy(raw_credits_path, self.data_ingestion_config.credits_data_path)

            
            movies_df = pd.read_csv(self.data_ingestion_config.movies_data_path)
            credits_df = pd.read_csv(self.data_ingestion_config.credits_data_path)

            # merge both the dfs

            final_df = movies_df.merge(credits_df, on="title")

            final_df.to_csv(self.data_ingestion_config.final_data_path, index=False)

            data_ingestion_artifacts = DataIngestionArtifacts(movies_file_path=self.data_ingestion_config.movies_data_path,
                                                              credits_file_path=self.data_ingestion_config.credits_data_path,
                                                              final_data_path=self.data_ingestion_config.final_data_path)
            return data_ingestion_artifacts
        except Exception as e:
            logging.info(CustomException(e, sys))
            raise CustomException(e, sys)
        