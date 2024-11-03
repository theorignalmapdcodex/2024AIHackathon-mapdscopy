import numpy as np
from mm_rag.video_embedding_data import VideoEmbeddingData


class EmbeddingBase:
    def __init__(self) -> None:
        pass

    def embed(self, MultiModalData) -> VideoEmbeddingData:
        pass
