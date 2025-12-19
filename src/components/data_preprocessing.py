from src.logging.logger import logging
from src.exception_handling.exception import CustomException
from src.constants import training_pipeline
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataProcessingConfig
from src.entity.artifact_entity import DataIngestionArtifacts, DataProcessingArtifacts
from nltk.stem import PorterStemmer
import pandas as pd
import sys, os
import ast

class DataProcessing:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig, data_ingestion_artifacts: DataIngestionArtifacts,
                 data_processing_config: DataProcessingConfig):
        self.training_pipeline_config = training_pipeline_config
        self.data_ingestion_artifacts = data_ingestion_artifacts
        self.data_processing_config = data_processing_config
        self.ps = PorterStemmer()

    def get_genres(self, obj):
        try:
            L = []
            for i in ast.literal_eval(obj):
              L.append(i['name'])
            return L
        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e,sys)
        
    def get_keywords(self, obj):
        try:
            L = []
            for i in ast.literal_eval(obj):
              L.append(i['name'])
            return L
        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e,sys)
    
    def get_cast(self, obj):
        try:
            L= []
            counter = 0
            for i in ast.literal_eval(obj):
                if counter != 3:
                    L.append(i["name"])
                    counter +=1
                else:
                    break
            return L
        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e,sys)
        
    def get_crew(self, obj):
        try:
            L=[]
            for i in ast.literal_eval(obj):
                if i["job"] == "Director":
                    L.append(i["name"])
            return L
        except Exception as e:
            print(e)

    def stem_text(self, text):
        try:
            words = text.split()
            return " ".join([self.ps.stem(word) for word in words])
        except Exception as e:
            logging.info(CustomException(e, sys))
            raise CustomException(e,sys)


    def initiate_processing(self)->DataProcessingArtifacts:
        try:
            os.makedirs(self.data_processing_config.data_processing_dir, exist_ok=True)
            logging.info("Reading from the data ingestion_artifacts ie final_data")
            df = pd.read_csv(self.data_ingestion_artifacts.final_data_path)

            logging.info("Removing the unnecessary columns")
            df = df[training_pipeline.COLUMNS]

            logging.info("Dropping the null values")
            df.dropna(inplace=True)

            logging.info("Processing the text columns to obtain meaningful informations")

            df["genres"] = df["genres"].apply(self.get_genres)
            df["keywords"] = df["keywords"].apply(self.get_keywords)

            df["cast"] = df["cast"].apply(self.get_cast)
            df["crew"] = df["crew"].apply(self.get_crew)


            df["overview"] = df["overview"].apply(lambda x:x.split())

            df["cast"] = df["cast"].apply(lambda x:[i.replace(" ","") for i in x])
            df["crew"] = df["crew"].apply(lambda x:[i.replace(" ","") for i in x])
            df["keywords"] = df["keywords"].apply(lambda x:[i.replace(" ","") for i in x])
            df["genres"] = df["genres"].apply(lambda x:[i.replace(" ","") for i in x])

            logging.info("Add all these columns into 1")
            df["tags"] = df["cast"] + df["crew"] + df["keywords"] + df["genres"] + df["overview"]

            df = df[["movie_id", "title", "tags"]]

            df["tags"] = df["tags"].apply(lambda x:" ".join(x))
            df["tags"] = df["tags"].apply(lambda x: x.lower())
            df["tags"] = df["tags"].apply(self.stem_text)
            df.to_csv(self.data_processing_config.final_df, index=False)

            data_processing_artifacts = DataProcessingArtifacts(final_df=self.data_processing_config.final_df)

            return data_processing_artifacts



            


        except Exception as e:
            logging.info(CustomException(e,sys))
            raise CustomException(e,sys)
        