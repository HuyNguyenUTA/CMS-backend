from qdrant_client import QdrantClient
from app.core.config import settings
from openai import OpenAI

client = QdrantClient(
    url=settings.QDRANT_HOST,
    api_key=settings.QDRANT_API_KEY
)

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

def embed_text(text):
    return openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    ).data[0].embedding

def retrieve_from_qdrant(restaurant_id: str, query: str, top_k: int = 3):
    vector = embed_text(query)
    results = client.search(
        collection_name=restaurant_id,
        query_vector=vector,
        limit=top_k
    )
    return "\n".join([hit.payload["text"] for hit in results])
