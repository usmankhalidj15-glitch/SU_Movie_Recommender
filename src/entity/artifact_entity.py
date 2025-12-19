from dataclasses import dataclass


@dataclass
class DataIngestionArtifacts:
    movies_file_path: str
    credits_file_path: str
    final_data_path: str


@dataclass
class DataProcessingArtifacts:
    final_df: str

@dataclass
class RecomenderTrainingrArtifacts:
    """
    Artifacts produced by the recommender training stage.

    - vectorizer_path: path to the fitted text vectorizer
    - similarity_matrix_content_path: content-based cosine similarity matrix (current default)
    - similarity_matrix_alt_path: optional alternative similarity matrix
    """
    vectorizer_path: str
    similarity_matrix_content_path: str
    similarity_matrix_alt_path: str

@dataclass
class RecoomendArtifacts:
    movies : list