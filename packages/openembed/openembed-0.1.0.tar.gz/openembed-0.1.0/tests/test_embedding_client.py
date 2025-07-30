"""Tests for the EmbeddingClient class."""

import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from src.openembed import EmbeddingClient
from src.openembed.providers.base import Provider
from src.openembed.utils.errors import ModelNotFoundError


class MockProvider(Provider):
    """Mock provider for testing."""

    def __init__(self, config=None):
        super().__init__(config)
        self.create_embedding_called = False
        self.batch_create_embeddings_called = False

    def create_embedding(self, input_data, model_name, **kwargs):
        """Mock create_embedding method."""
        self.create_embedding_called = True
        return [0.1, 0.2, 0.3, 0.4, 0.5]

    def batch_create_embeddings(self, inputs, model_name, **kwargs):
        """Mock batch_create_embeddings method."""
        self.batch_create_embeddings_called = True
        return [[0.1, 0.2, 0.3, 0.4, 0.5] for _ in inputs]

    def supports_model(self, model_name):
        """Mock supports_model method."""
        return model_name == "mock-model"

    def supported_models(self):
        """Mock supported_models method."""
        return ["mock-model"]

    def supported_input_types(self):
        """Mock supported_input_types method."""
        return ["text"]


class TestEmbeddingClient(unittest.TestCase):
    """Tests for the EmbeddingClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = EmbeddingClient()
        self.mock_provider = MockProvider()
        self.client.register_provider("mock", self.mock_provider)

    def test_register_provider(self):
        """Test registering a provider."""
        self.assertIn("mock", self.client.providers)
        self.assertEqual(self.client.providers["mock"], self.mock_provider)

    def test_create_embedding(self):
        """Test creating an embedding."""
        embedding = self.client.create_embedding("test", model_name="mock-model")
        self.assertTrue(self.mock_provider.create_embedding_called)
        self.assertEqual(embedding, [0.1, 0.2, 0.3, 0.4, 0.5])

    def test_batch_create_embeddings(self):
        """Test creating embeddings in batch."""
        inputs = ["test1", "test2", "test3"]
        embeddings = self.client.batch_create_embeddings(inputs, model_name="mock-model")
        self.assertTrue(self.mock_provider.batch_create_embeddings_called)
        self.assertEqual(len(embeddings), len(inputs))
        self.assertEqual(embeddings[0], [0.1, 0.2, 0.3, 0.4, 0.5])

    def test_model_not_found(self):
        """Test error when model is not found."""
        with self.assertRaises(ModelNotFoundError):
            self.client.create_embedding("test", model_name="nonexistent-model")

    def test_caching(self):
        """Test caching functionality."""
        # Create a client with caching enabled
        client = EmbeddingClient(cache_enabled=True)
        client.register_provider("mock", self.mock_provider)
        
        # Mock the cache manager
        client.cache_manager.get = MagicMock(return_value=None)
        client.cache_manager.set = MagicMock()
        
        # First call should check cache and then set it
        embedding = client.create_embedding("test", model_name="mock-model")
        client.cache_manager.get.assert_called_once()
        client.cache_manager.set.assert_called_once()
        
        # Reset mocks
        client.cache_manager.get.reset_mock()
        client.cache_manager.set.reset_mock()
        
        # Second call with same input should get from cache
        client.cache_manager.get = MagicMock(return_value=[0.1, 0.2, 0.3, 0.4, 0.5])
        embedding = client.create_embedding("test", model_name="mock-model")
        client.cache_manager.get.assert_called_once()
        client.cache_manager.set.assert_not_called()


if __name__ == "__main__":
    unittest.main()