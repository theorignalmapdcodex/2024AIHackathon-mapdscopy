from mm_rag.vector_db.pinecone_db import PineconeDB

from mm_rag.video_embedding_data import VideoEmbeddingData

def test_insert():
    # Test the insert function of the PineconeDB class
    pinecone_db = PineconeDB()

    # Create a dummy list of VideoEmbeddingData objects
    embedding_list = [
        VideoEmbeddingData(
            video_id="video_1",
            embedding=[1.0] * 1408,
            start_offset_sec=0,
            end_offset_sec=10,
        ),
        VideoEmbeddingData(
            video_id="video_2",
            embedding=[2.0] * 1408,
            start_offset_sec=10,
            end_offset_sec=20,
        ),
    ]

    result = pinecone_db.insert(embedding_list)

    # Check if the insert was successful
    assert result["upserted_count"] == 2

    # delete the inserted embeddings, so we are good to go
    pinecone_db.index.delete(ids=[record.video_id for record in embedding_list], namespace="video")

def test_query():
    # Test the query function of the PineconeDB class
    pinecone_db = PineconeDB()

    # Create a dummy embedding
    embedding = [1.0] * 1408

    result = pinecone_db.search(embedding)

    assert type(result) == list
    assert len(result) > 0
    assert len(result[0]["values"]) > 0
    assert result[0]["start_offset_sec"] >= 0
    assert result[0]["end_offset_sec"] >= 1
    assert result[0]["score"] >= 0.0