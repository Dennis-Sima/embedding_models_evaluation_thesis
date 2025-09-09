from typing import List
from tqdm import tqdm
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore


def create_embedding_model(model_name: str) -> HuggingFaceEmbeddings:
    """Initialize and return a HuggingFace embedding model."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"trust_remote_code": True},
        encode_kwargs={"normalize_embeddings": False},
    )


def reset_collection(qdrant: QdrantClient, collection_name: str, vector_size: int) -> None:
    """Drop the collection if it exists and recreate it with the given vector size."""
    existing_collections = [col.name for col in qdrant.get_collections().collections]

    if collection_name in existing_collections:
        print(f"Deleting existing collection '{collection_name}'...")
        qdrant.delete_collection(collection_name=collection_name)

    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )


def import_activities(
    activities: List[str],
    model_name: str,
    collection: str,
    host: str = "localhost",
    port: int = 6333,
    batch_size: int = 64,
) -> None:
    """
    Embed activities and store them in a Qdrant collection.

    Args:
        activities: List of activity texts.
        model_name: HuggingFace embedding model name.
        collection: Target Qdrant collection name.
        host: Qdrant host (default: localhost).
        port: Qdrant port (default: 6333).
        batch_size: Number of texts to insert per batch.
    """
    # Initialize embedding model
    embeddings = create_embedding_model(model_name)

    # Detect vector size of embedding model
    vector_size = len(embeddings.embed_query("test"))

    client = QdrantClient(host=host, port=port)

    # Ensure fresh collection
    reset_collection(client, collection, vector_size)

    # Initialize vector store
    store = QdrantVectorStore(
        client=client,
        collection_name=collection,
        embedding=embeddings,
    )

    # Batch insert activities
    print(f"Uploading {len(activities)} activities to collection '{collection}'...")
    for i in tqdm(range(0, len(activities), batch_size), desc="Embedding batches"):
        batch = activities[i:i + batch_size]
        store.add_texts(batch)

    # Quick validation
    results = store.similarity_search("test query", k=3)
    print(f"Imported {len(activities)} activities using model '{model_name}'")
    print(f"Example search returned {len(results)} results")
