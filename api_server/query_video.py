from mm_rag.embedding.vertex_embedding import VertexEmbedding
from mm_rag.vector_db.pinecone_db import PineconeDB

def main(query: str):
    # Extract query embeddings
    ve = VertexEmbedding()
    embeddings = ve.embed_text(query)

    # query top k embeddings from Pinecone
    pdb = PineconeDB()
    results = pdb.search(embeddings.embedding)

    return results


if __name__ == "__main__":
    query = "The name of the first leading astronaut"
    result = main(query)
    for r in result:
        print(r["id"], r["score"])
