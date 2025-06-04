import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

restaurant_id = "sakura-ramen"  # collection name in Qdrant

# Init clients
qdrant = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text):
    return openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    ).data[0].embedding

# Read and chunk the menu
with open("data/menu.txt", "r") as f:
    raw = f.read()

chunks = [chunk.strip() for chunk in raw.split("\n\n") if chunk.strip()]

# Create collection (if not exists)
qdrant.recreate_collection(
    collection_name=restaurant_id,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Upload each chunk
points = [
    PointStruct(id=i, vector=get_embedding(chunk), payload={"text": chunk})
    for i, chunk in enumerate(chunks)
]

qdrant.upsert(collection_name=restaurant_id, points=points)

print(f"✅ Ingested {len(points)} chunks to Qdrant collection: {restaurant_id}")
