from sentence_transformers import SentenceTransformer

# Load model once (IMPORTANT for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts):
    """
    texts: list of strings
    returns: list of embedding vectors
    """
    return model.encode(texts).tolist()

def embed_query(text):
    """
    text: single string
    returns: single embedding vector
    """
    return model.encode([text])[0].tolist()