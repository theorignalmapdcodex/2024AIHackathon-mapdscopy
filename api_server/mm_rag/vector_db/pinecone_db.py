import os
from typing import List
from pinecone import Pinecone
from mm_rag.image_embedding_data import ImageEmbeddingData
from mm_rag.video_embedding_data import VideoEmbeddingData

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

class PineconeDB:
    def __init__(self, db_name="mmrag"):
        self.client = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.client.Index(db_name)

    def insert(self, embedding_list: List[VideoEmbeddingData]):
        vector = []
        for record in embedding_list:
            vector.append(
                {
                    "id": record.video_id,
                    "values": record.embedding,
                    "metadata": {
                        "start_offset_sec": record.start_offset_sec,
                        "end_offset_sec": record.end_offset_sec,
                    },
                }
            )

        upsert_response = self.index.upsert(vectors=vector, namespace="video")

        return upsert_response

    def insert_image(self, embedding_list: List[ImageEmbeddingData]):
        vector = []
        for record in embedding_list:
            vector.append(
                {
                    "id": record.image_id,
                    "values": record.embedding,
                }
            )
        upsert_response = self.index.upsert(vectors=vector, namespace="image")

        return upsert_response

    def search(self, embedding: List[float], top_k=5):
        search_response = self.index.query(
            namespace="video",
            vector=embedding,
            top_k=top_k,
            # filter={"genre": {"$eq": "documentary"}},
            include_values=True,
            include_metadata=True,
        )

        matches = []
        for match in search_response["matches"]:
            matches.append(
                {
                    "id": match["id"],
                    "values": match["values"],
                    "start_offset_sec": match["metadata"]["start_offset_sec"],
                    "end_offset_sec": match["metadata"]["end_offset_sec"],
                    "score": match["score"],
                }
            )

        return matches
