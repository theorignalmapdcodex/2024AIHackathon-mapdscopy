from mm_rag.embedding.vertex_embedding import VertexEmbedding
from mm_rag.multi_modal_data import MultiModalData
from mm_rag.vector_db.pinecone_db import PineconeDB

def main(image_url: str):
    # Extract query embeddings
    ve = VertexEmbedding()
    embeddings = ve.embed_image(MultiModalData(data_uri=image_url))

    # query top k embeddings from Pinecone
    pdb = PineconeDB()
    results = pdb.search(embeddings.embedding)

    return results


if __name__ == "__main__":
    query_image = "jon.jpg"
    result = main(query_image)
    for r in result:
        print(r["id"], r["score"])
