from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from documents.models import DocumentChunk
import os
from vectorstore.embeddings import generate_embeddings, embed_query
from dotenv import load_dotenv
load_dotenv()

INDEX_DIMENSION = 384
def connect_index():
    pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))
    index = pc.Index("final-project")
    return index
    
def upsert_index():
    document = DocumentChunk.objects.all()
    vector_records = []
    for chunk in document:
        text = chunk.chunk_text
        vectors = generate_embeddings([text])
        embedding_vector = vectors[0]
        
        if len(embedding_vector) != INDEX_DIMENSION:
             raise ValueError(
                f"Embedding dimension mismatch for chunk {chunk.id}: "
                f"expected {INDEX_DIMENSION}, got {len(embedding_vector)}"
            )
        id = f"{chunk.policy_document.policy_title}_{str(chunk.chunk_index)}"
    
        vector_record = {
           "id" : id,
           "values" : embedding_vector,
           "metadata" : {
               "text" : text,
               "source" : chunk.policy_document.policy_title,
           }
        }
        vector_records.append(vector_record)
    if not vector_records:
        print("No vectors to upsert!")
        return None
    index = connect_index()
    upsert_records =index.upsert(vectors = vector_records, namespace="default")
    print(len(vector_records))
    return upsert_records

def search_chunks(question):
    query_vector = embed_query(question)
    if len(query_vector) != INDEX_DIMENSION:
        raise ValueError(
            f"Query vector dimension mismatch: expected {INDEX_DIMENSION}, got {len(query_vector)}"
        )

    result = connect_index().query(
        vector=query_vector,
        top_k=5,  
        include_metadata=True,
        namespace="default"
    )

    print("RAW RESPONSE:", result)

    matches = result.get("matches", [])
    print("MATCH COUNT:", len(matches))

    for m in matches:
        print("\n--- MATCH ---")
        print(m["metadata"]["text"][:300])

    return matches
