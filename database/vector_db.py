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
    port: int = 6333
) -> None:
    """
    Embed activities and store them in a Qdrant collection.

    Args:
        activities: List of activity texts.
        model_name: HuggingFace embedding model name.
        collection: Target Qdrant collection name.
        host: Qdrant host (default: localhost).
        port: Qdrant port (default: 6333).
    """
    # Initialize embedding model
    embeddings = create_embedding_model(model_name)

    # Detect vector size of embedding model
    vector_size = len(embeddings.embed_query("test"))

    client = QdrantClient(host=host, port=port)

    # Ensure fresh collection
    reset_collection(client, collection, vector_size)

    # Initialize vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection,
        embedding=embeddings,
    )

    print("Embedding and uploading activities to Qdrant...")
    for activity_text in tqdm(activities, desc="Processing activities"):
        vector_store.add_texts([activity_text])

    test_results = vector_store.similarity_search("test query", k=1000000)
    print(f"Loaded {len(test_results)} activities into vector store: '{model_name}'")
