import pathlib
from mm_rag.data_storage.google_storage import GoogleStorage
from mm_rag.embedding.vertex_embedding import VertexEmbedding
from mm_rag.vector_db.pinecone_db import PineconeDB


def main(input_video_path: pathlib.Path):
    # Upload video to Google Cloud Storage
    gs = GoogleStorage()
    video_gs_path = gs.upload_video(input_video_path)

    print(video_gs_path)

    # Extract video embeddings
    ve = VertexEmbedding()
    embeddings = ve.embed_video(video_gs_path)

    # Save embeddings to Pinecone
    pdb = PineconeDB()
    pdb.insert(embeddings)

    return video_gs_path


if __name__ == "__main__":
    CURRENT_DIR = pathlib.Path(__file__).resolve().parent
    main(CURRENT_DIR / "mm_rag/data_storage/data/Welcome back to Planet Earth.mp4")
