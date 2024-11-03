from mm_rag.embedding.vertex_embedding import VertexEmbedding

from mm_rag.multi_modal_data import MultiModalData
from mm_rag.text_embedding_data import TextEmbeddingData

def test_video():
    # Test the main function of the script
    ve = VertexEmbedding()

    result = ve.embed_video(MultiModalData(data_uri="gs://mmrag/90_welcome-back-to-planet-earth.mp4", duration=90))

    assert type(result) == list
    assert len(result) > 0
    assert ".mp4" in result[0].video_id
    assert len(result[0].embedding) > 0
    assert result[0].start_offset_sec >= 0
    assert result[0].end_offset_sec >= 1

def test_text():
    ve = VertexEmbedding()

    result = ve.embed_text("Hello, world!")

    assert type(result) == TextEmbeddingData
    assert len(result.embedding) > 0
    assert result.text == "Hello, world!"