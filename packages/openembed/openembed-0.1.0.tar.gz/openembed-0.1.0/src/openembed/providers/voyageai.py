"""VoyageAI provider for embedding models."""

import logging
from typing import Any, Dict, List, Optional, Union, cast

try:
    import voyageai
    VOYAGEAI_AVAILABLE = True
except ImportError:
    VOYAGEAI_AVAILABLE = False

from openembed.providers.base import Provider, InputType, EmbeddingType
from openembed.utils.errors import (
    ProviderError,
    ModelNotFoundError,
    AuthenticationError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class VoyageAIProvider(Provider):
    """Provider for VoyageAI embedding models."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the VoyageAI provider.

        Args:
            config: Configuration for the VoyageAI API.
                Example: {"api_key": "..."}
        """
        super().__init__(config)
        
        if not VOYAGEAI_AVAILABLE:
            logger.warning(
                "VoyageAI package not installed. Install it with 'pip install voyageai'"
            )
            return

        self.client = self._initialize_client()
        self._models = {
            "voyage-large-2": {
                "dimensions": 1024,
                "input_types": ["text"],
            },
            "voyage-code-2": {
                "dimensions": 1024,
                "input_types": ["text"],
            },
            "voyage-large-2-instruct": {
                "dimensions": 1024,
                "input_types": ["text"],
            },
        }

    def _initialize_client(self) -> Optional[voyageai.Client]:
        """Initialize the VoyageAI client.

        Returns:
            The VoyageAI client instance.

        Raises:
            AuthenticationError: If the API key is not provided.
        """
        if not VOYAGEAI_AVAILABLE:
            return None

        api_key = self.config.get("api_key")
        if not api_key:
            logger.warning("VoyageAI API key not provided")
            return None

        return voyageai.Client(api_key=api_key)

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
            ProviderError: If there's an error from the VoyageAI API.
        """
        if not VOYAGEAI_AVAILABLE:
            raise ImportError(
                "VoyageAI package not installed. Install it with 'pip install voyageai'"
            )

        if not self.client:
            raise AuthenticationError("VoyageAI client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            response = self.client.embed(
                input=input_data,
                model=model_name,
                **kwargs
            )
            return cast(List[float], response["embeddings"][0])
        except voyageai.error.RateLimitError as e:
            raise RateLimitError(f"VoyageAI rate limit exceeded: {str(e)}")
        except voyageai.error.AuthenticationError as e:
            raise AuthenticationError(f"VoyageAI authentication error: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Error creating embedding with VoyageAI: {str(e)}")

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
            ProviderError: If there's an error from the VoyageAI API.
        """
        if not VOYAGEAI_AVAILABLE:
            raise ImportError(
                "VoyageAI package not installed. Install it with 'pip install voyageai'"
            )

        if not self.client:
            raise AuthenticationError("VoyageAI client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            response = self.client.embed(
                input=inputs,
                model=model_name,
                **kwargs
            )
            return cast(List[List[float]], response["embeddings"])
        except voyageai.error.RateLimitError as e:
            raise RateLimitError(f"VoyageAI rate limit exceeded: {str(e)}")
        except voyageai.error.AuthenticationError as e:
            raise AuthenticationError(f"VoyageAI authentication error: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Error creating embeddings with VoyageAI: {str(e)}")