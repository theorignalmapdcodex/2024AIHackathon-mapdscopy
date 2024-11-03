import os
from typing import List
from mm_rag.image_embedding_data import ImageEmbeddingData
from mm_rag.video_embedding_data import VideoEmbeddingData
from mm_rag.text_embedding_data import TextEmbeddingData
from mm_rag.multi_modal_data import MultiModalData
import vertexai

from vertexai.vision_models import MultiModalEmbeddingModel, Video, Image
from vertexai.vision_models import VideoSegmentConfig

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
vertexai.init(project=PROJECT_ID, location="us-central1")


class VertexEmbedding:
    def __init__(self, interval_sec=10) -> None:
        self.model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
        self.interval_sec = interval_sec

    def embed_video(self, data: MultiModalData) -> List[VideoEmbeddingData]:
        embeddings = self.model.get_embeddings(
            video=Video.load_from_file(data.data_uri),
            video_segment_config=VideoSegmentConfig(
                start_offset_sec=0,
                end_offset_sec=data.duration,
                interval_sec=self.interval_sec,
            ),
        )

        result = []
        for video_embedding in embeddings.video_embeddings:
            video_id = f"{data.data_uri}_{video_embedding.start_offset_sec}_{video_embedding.end_offset_sec}"
            data_item = VideoEmbeddingData(
                video_id=video_id,
                embedding=video_embedding.embedding, # vector of 1408 elements
                start_offset_sec=video_embedding.start_offset_sec,
                end_offset_sec=video_embedding.end_offset_sec,
            )

            result.append(data_item)

        return result

    def embed_text(self, data: str) -> TextEmbeddingData:
        embeddings = self.model.get_embeddings(contextual_text=data)

        return TextEmbeddingData(
            embedding=embeddings.text_embedding, # vector of 1408 elements
            text=data,
        )

    def embed_image(self, data: MultiModalData) -> ImageEmbeddingData:
        embeddings = self.model.get_embeddings(image=Image.load_from_file(data.data_uri))

        return ImageEmbeddingData(
            embedding=embeddings.image_embedding, # vector of 1408 elements
            image_id=data.data_uri,
        )