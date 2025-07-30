"""Cohere provider for embedding models."""

import logging
from typing import Any, Dict, List, Optional, Union, cast

try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False

from openembed.providers.base import Provider, InputType, EmbeddingType
from openembed.utils.errors import (
    ProviderError,
    ModelNotFoundError,
    AuthenticationError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class CohereProvider(Provider):
    """Provider for Cohere embedding models."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Cohere provider.

        Args:
            config: Configuration for the Cohere API.
                Example: {"api_key": "..."}
        """
        super().__init__(config)
        
        if not COHERE_AVAILABLE:
            logger.warning(
                "Cohere package not installed. Install it with 'pip install cohere'"
            )
            return

        self.client = self._initialize_client()
        self._models = {
            "embed-english-v2.0": {
                "dimensions": 4096,
                "input_types": ["text"],
            },
            "embed-english-light-v2.0": {
                "dimensions": 1024,
                "input_types": ["text"],
            },
            "embed-multilingual-v2.0": {
                "dimensions": 768,
                "input_types": ["text"],
            },
        }

    def _initialize_client(self) -> Optional[cohere.Client]:
        """Initialize the Cohere client.

        Returns:
            The Cohere client instance.

        Raises:
            AuthenticationError: If the API key is not provided.
        """
        if not COHERE_AVAILABLE:
            return None

        api_key = self.config.get("api_key")
        if not api_key:
            logger.warning("Cohere API key not provided")
            return None

        return cohere.Client(api_key)

    def supports_model(self, model_name: str) -> bool:
        """Check if this provider supports the given model.

        Args:
            model_name: The name of the model to check.

        Returns:
            True if the provider supports the model, False otherwise.
        """
        return model_name in self._models

    def supported_models(self) -> List[str]:
        """Get the list of models supported by this provider.

        Returns:
            List of supported model names.
        """
        return list(self._models.keys())

    def supported_input_types(self) -> List[str]:
        """Get the list of input types supported by this provider.

        Returns:
            List of supported input types.
        """
        return ["text"]

    def create_embedding(
        self, input_data: InputType, model_name: str, **kwargs
    ) -> EmbeddingType:
        """Create an embedding for the given input.

        Args:
            input_data: The processed input to create an embedding for.
            model_name: The name of the model to use.
            **kwargs: Additional model-specific parameters.

        Returns:
            The embedding vector.

        Raises:
            ModelNotFoundError: If the model is not supported.
            ProviderError: If there's an error from the Cohere API.
        """
        if not COHERE_AVAILABLE:
            raise ImportError(
                "Cohere package not installed. Install it with 'pip install cohere'"
            )

        if not self.client:
            raise AuthenticationError("Cohere client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            # Cohere expects a list of texts, even for a single input
            texts = [input_data] if isinstance(input_data, str) else input_data
            response = self.client.embed(
                texts=texts,
                model=model_name,
                **kwargs
            )
            # Return the first embedding for a single input
            return cast(List[float], response.embeddings[0])
        except cohere.error.CohereError as e:
            if "rate limit" in str(e).lower():
                raise RateLimitError(f"Cohere rate limit exceeded: {str(e)}")
            elif "auth" in str(e).lower() or "key" in str(e).lower():
                raise AuthenticationError(f"Cohere authentication error: {str(e)}")
            else:
                raise ProviderError(f"Error creating embedding with Cohere: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Error creating embedding with Cohere: {str(e)}")

    def batch_create_embeddings(
        self, inputs: List[InputType], model_name: str, **kwargs
    ) -> List[EmbeddingType]:
        """Create embeddings for multiple inputs in a batch.

        Args:
            inputs: List of processed inputs to create embeddings for.
            model_name: The name of the model to use.
            **kwargs: Additional model-specific parameters.

        Returns:
            List of embedding vectors.

        Raises:
            ModelNotFoundError: If the model is not supported.
            ProviderError: If there's an error from the Cohere API.
        """
        if not COHERE_AVAILABLE:
            raise ImportError(
                "Cohere package not installed. Install it with 'pip install cohere'"
            )

        if not self.client:
            raise AuthenticationError("Cohere client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            # Flatten inputs if they are lists of strings
            texts = []
            for input_data in inputs:
                if isinstance(input_data, str):
                    texts.append(input_data)
                elif isinstance(input_data, list) and all(isinstance(item, str) for item in input_data):
                    texts.extend(input_data)
                else:
                    raise ValueError(f"Unsupported input type: {type(input_data)}")
            
            response = self.client.embed(
                texts=texts,
                model=model_name,
                **kwargs
            )
            return cast(List[List[float]], response.embeddings)
        except cohere.error.CohereError as e:
            if "rate limit" in str(e).lower():
                raise RateLimitError(f"Cohere rate limit exceeded: {str(e)}")
            elif "auth" in str(e).lower() or "key" in str(e).lower():
                raise AuthenticationError(f"Cohere authentication error: {str(e)}")
            else:
                raise ProviderError(f"Error creating embeddings with Cohere: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Error creating embeddings with Cohere: {str(e)}")