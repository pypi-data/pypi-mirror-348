"""Basic usage examples for the OpenEmbed library."""

import os
import sys
import numpy as np
from pathlib import Path

# Add the parent directory to the path so we can import the library
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.openembed import EmbeddingClient


def print_embedding_info(embedding, model_name):
    """Print information about an embedding."""
    print(f"\nEmbedding from {model_name}:")
    print(f"  Type: {type(embedding)}")
    print(f"  Shape: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
    print(f"  Norm: {np.linalg.norm(embedding)}")


def basic_example():
    """Basic example of using the OpenEmbed library."""
    print("OpenEmbed Basic Example")
    print("======================")

    # Initialize the client
    client = EmbeddingClient()

    # Example text
    text = "This is a sample text for embedding."

    # Try different models if available
    models_to_try = [
        # OpenAI
        "text-embedding-ada-002",
        # Cohere
        "embed-english-v2.0",
        # HuggingFace
        "sentence-transformers/all-MiniLM-L6-v2",
        # VoyageAI
        "voyage-large-2",
        # Amazon
        "amazon.titan-embed-text-v1",
    ]

    for model_name in models_to_try:
        try:
            # Create embedding
            embedding = client.create_embedding(text, model_name=model_name)
            print_embedding_info(embedding, model_name)
        except Exception as e:
            print(f"\nError with {model_name}: {str(e)}")


def batch_example():
    """Example of batch embedding."""
    print("\nOpenEmbed Batch Example")
    print("======================")

    # Initialize the client
    client = EmbeddingClient()

    # Example texts
    texts = [
        "This is the first document.",
        "This is the second document.",
        "And this is the third one.",
        "Is this the first document?",
    ]

    # Use OpenAI for this example
    try:
        model_name = "text-embedding-ada-002"
        
        # Create embeddings
        embeddings = client.batch_create_embeddings(texts, model_name=model_name)
        
        print(f"\nBatch embeddings from {model_name}:")
        print(f"  Number of embeddings: {len(embeddings)}")
        print(f"  Shape of first embedding: {len(embeddings[0])}")
        
        # Calculate similarity matrix
        similarity_matrix = np.zeros((len(embeddings), len(embeddings)))
        for i in range(len(embeddings)):
            for j in range(len(embeddings)):
                similarity_matrix[i, j] = np.dot(embeddings[i], embeddings[j])
        
        print("\nSimilarity matrix:")
        for i in range(len(texts)):
            print(f"  {texts[i]}")
        print("\n  " + " ".join([f"{i+1:^7}" for i in range(len(texts))]))
        for i in range(len(similarity_matrix)):
            print(f"  {i+1} " + " ".join([f"{similarity_matrix[i, j]:^7.4f}" for j in range(len(similarity_matrix))]))
    
    except Exception as e:
        print(f"\nError with batch embedding: {str(e)}")


def caching_example():
    """Example of using caching."""
    print("\nOpenEmbed Caching Example")
    print("========================")

    # Initialize the client with caching enabled
    client = EmbeddingClient(cache_enabled=True)

    # Example text
    text = "This is a sample text for embedding."
    model_name = "text-embedding-ada-002"

    try:
        # First call (not cached)
        print("\nFirst call (not cached):")
        import time
        start_time = time.time()
        embedding1 = client.create_embedding(text, model_name=model_name)
        elapsed_time1 = time.time() - start_time
        print(f"  Time: {elapsed_time1:.4f} seconds")

        # Second call (should be cached)
        print("\nSecond call (should be cached):")
        start_time = time.time()
        embedding2 = client.create_embedding(text, model_name=model_name)
        elapsed_time2 = time.time() - start_time
        print(f"  Time: {elapsed_time2:.4f} seconds")
        print(f"  Speedup: {elapsed_time1 / elapsed_time2:.2f}x")

        # Verify embeddings are the same
        print(f"  Embeddings are identical: {np.array_equal(embedding1, embedding2)}")

        # Clear cache
        client.clear_cache()
        print("\nCache cleared.")

        # Third call (not cached again)
        print("\nThird call (after clearing cache):")
        start_time = time.time()
        embedding3 = client.create_embedding(text, model_name=model_name)
        elapsed_time3 = time.time() - start_time
        print(f"  Time: {elapsed_time3:.4f} seconds")
        print(f"  Embeddings are identical: {np.array_equal(embedding1, embedding3)}")

    except Exception as e:
        print(f"\nError with caching example: {str(e)}")


if __name__ == "__main__":
    basic_example()
    batch_example()
    caching_example()