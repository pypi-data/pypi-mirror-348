"""Main client interface for the OpenEmbed library."""

import logging
from typing import Any, Dict, List, Optional, Union, Type

from openembed.providers.base import Provider
from openembed.providers.openai import OpenAIProvider
from openembed.providers.cohere import CohereProvider
from openembed.providers.huggingface import HuggingFaceProvider
from openembed.providers.voyageai import VoyageAIProvider
from openembed.providers.amazon import AmazonTitanProvider
from openembed.processors.base import InputProcessor
from openembed.processors.text import TextProcessor
from openembed.cache.base import CacheManager
from openembed.cache.memory import MemoryCache
from openembed.cache.disk import DiskCache
from openembed.utils.errors import ModelNotFoundError, ProviderError

logger = logging.getLogger(__name__)

InputType = Union[str, List[str], Dict[str, Any]]
EmbeddingType = List[float]


class EmbeddingClient:
    """Main client for creating embeddings from different providers."""

    def __init__(
        self,
        provider_config: Optional[Dict[str, Dict[str, Any]]] = None,
        cache_enabled: bool = True,
        cache_dir: Optional[str] = None,
    ):
        """Initialize the embedding client.

        Args:
            provider_config: Configuration for different providers.
                Example: {"openai": {"api_key": "sk-..."}}
            cache_enabled: Whether to enable caching.
            cache_dir: Directory to store cache files.
        """
        self.provider_config = provider_config or {}
        self.cache_enabled = cache_enabled
        self.cache_dir = cache_dir

        # Initialize providers
        self.providers: Dict[str, Provider] = {}
        self._register_default_providers()

        # Initialize processors
        self.processors: Dict[str, InputProcessor] = {}
        self._register_default_processors()

        # Initialize cache
        self.cache_manager = self._initialize_cache()

    def _register_default_providers(self) -> None:
        """Register the default providers."""
        self.register_provider("openai", OpenAIProvider(self.provider_config.get("openai", {})))
        self.register_provider("cohere", CohereProvider(self.provider_config.get("cohere", {})))
        self.register_provider(
            "huggingface", HuggingFaceProvider(self.provider_config.get("huggingface", {}))
        )
        self.register_provider(
            "voyageai", VoyageAIProvider(self.provider_config.get("voyageai", {}))
        )
        self.register_provider(
            "amazon", AmazonTitanProvider(self.provider_config.get("amazon", {}))
        )

    def _register_default_processors(self) -> None:
        """Register the default input processors."""
        self.register_processor("text", TextProcessor())

    def _initialize_cache(self) -> CacheManager:
        """Initialize the cache manager."""
        if not self.cache_enabled:
            return None

        if self.cache_dir:
            return DiskCache(self.cache_dir)
        else:
            return MemoryCache()

    def register_provider(self, name: str, provider: Provider) -> None:
        """Register a provider.

        Args:
            name: The name of the provider.
            provider: The provider instance.
        """
        self.providers[name] = provider
        logger.debug(f"Registered provider: {name}")

    def register_processor(self, name: str, processor: InputProcessor) -> None:
        """Register an input processor.

        Args:
            name: The name of the processor.
            processor: The processor instance.
        """
        self.processors[name] = processor
        logger.debug(f"Registered processor: {name}")

    def _get_provider_for_model(self, model_name: str) -> Provider:
        """Get the provider for a specific model.

        Args:
            model_name: The name of the model.

        Returns:
            The provider instance.

        Raises:
            ModelNotFoundError: If no provider supports the model.
        """
        for provider in self.providers.values():
            if provider.supports_model(model_name):
                return provider

        raise ModelNotFoundError(f"No provider found for model: {model_name}")

    def _get_processor_for_input(self, input_data: InputType) -> InputProcessor:
        """Get the processor for a specific input type.

        Args:
            input_data: The input data.

        Returns:
            The processor instance.

        Raises:
            ValueError: If no processor supports the input type.
        """
        if isinstance(input_data, str):
            return self.processors["text"]
        elif isinstance(input_data, list) and all(isinstance(item, str) for item in input_data):
            return self.processors["text"]
        else:
            raise ValueError(f"Unsupported input type: {type(input_data)}")

    def _get_cache_key(self, input_data: InputType, model_name: str, **kwargs) -> str:
        """Generate a cache key for the input and model.

        Args:
            input_data: The input data.
            model_name: The name of the model.
            **kwargs: Additional parameters.

        Returns:
            The cache key.
        """
        # Simple implementation - in a real system, this would be more sophisticated
        if isinstance(input_data, str):
            return f"{input_data}:{model_name}:{kwargs}"
        elif isinstance(input_data, list):
            return f"{','.join(input_data)}:{model_name}:{kwargs}"
        else:
            return f"{str(input_data)}:{model_name}:{kwargs}"

    def create_embedding(
        self, input_data: InputType, model_name: str, use_cache: bool = True, **kwargs
    ) -> EmbeddingType:
        """Create an embedding for the given input.

        Args:
            input_data: The input to create an embedding for.
            model_name: The name of the model to use.
            use_cache: Whether to use the cache.
            **kwargs: Additional model-specific parameters.

        Returns:
            The embedding vector.

        Raises:
            ModelNotFoundError: If no provider supports the model.
            ProviderError: If there's an error from the provider.
        """
        # Check cache if enabled
        if self.cache_enabled and use_cache:
            cache_key = self._get_cache_key(input_data, model_name, **kwargs)
            cached_result = self.cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result

        # Get provider and processor
        provider = self._get_provider_for_model(model_name)
        processor = self._get_processor_for_input(input_data)

        # Process input
        processed_input = processor.process(input_data)

        # Create embedding
        embedding = provider.create_embedding(processed_input, model_name, **kwargs)

        # Cache result if enabled
        if self.cache_enabled and use_cache:
            cache_key = self._get_cache_key(input_data, model_name, **kwargs)
            self.cache_manager.set(cache_key, embedding)

        return embedding

    def batch_create_embeddings(
        self,
        inputs: List[InputType],
        model_name: str,
        batch_size: int = 32,
        use_cache: bool = True,
        **kwargs,
    ) -> List[EmbeddingType]:
        """Create embeddings for multiple inputs in a batch.

        Args:
            inputs: List of inputs to create embeddings for.
            model_name: The name of the model to use.
            batch_size: The batch size to use.
            use_cache: Whether to use the cache.
            **kwargs: Additional model-specific parameters.

        Returns:
            List of embedding vectors.

        Raises:
            ModelNotFoundError: If no provider supports the model.
            ProviderError: If there's an error from the provider.
        """
        # Get provider
        provider = self._get_provider_for_model(model_name)

        # Process inputs and check cache
        results = []
        uncached_inputs = []
        uncached_indices = []

        for i, input_data in enumerate(inputs):
            # Check cache if enabled
            if self.cache_enabled and use_cache:
                cache_key = self._get_cache_key(input_data, model_name, **kwargs)
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    results.append(cached_result)
                    continue

            # Process input
            processor = self._get_processor_for_input(input_data)
            processed_input = processor.process(input_data)
            uncached_inputs.append(processed_input)
            uncached_indices.append(i)
            # Add placeholder to results
            results.append(None)

        # If all results were cached, return them
        if not uncached_inputs:
            return results

        # Create embeddings for uncached inputs in batches
        for i in range(0, len(uncached_inputs), batch_size):
            batch_inputs = uncached_inputs[i : i + batch_size]
            batch_indices = uncached_indices[i : i + batch_size]

            # Create embeddings for batch
            batch_embeddings = provider.batch_create_embeddings(
                batch_inputs, model_name, **kwargs
            )

            # Store results and cache
            for j, embedding in enumerate(batch_embeddings):
                index = batch_indices[j]
                input_data = inputs[index]
                results[index] = embedding

                # Cache result if enabled
                if self.cache_enabled and use_cache:
                    cache_key = self._get_cache_key(input_data, model_name, **kwargs)
                    self.cache_manager.set(cache_key, embedding)

        return results

    def clear_cache(self) -> None:
        """Clear the cache."""
        if self.cache_enabled and self.cache_manager:
            self.cache_manager.clear()
            logger.debug("Cache cleared")