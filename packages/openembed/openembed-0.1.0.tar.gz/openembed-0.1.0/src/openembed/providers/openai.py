"""OpenAI provider for embedding models."""

import logging
from typing import Any, Dict, List, Optional, Union, cast

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from openembed.providers.base import Provider, InputType, EmbeddingType
from openembed.utils.errors import (
    ProviderError,
    ModelNotFoundError,
    AuthenticationError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class OpenAIProvider(Provider):
    """Provider for OpenAI embedding models."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the OpenAI provider.

        Args:
            config: Configuration for the OpenAI API.
                Example: {"api_key": "sk-...", "organization": "org-..."}
        """
        super().__init__(config)
        
        if not OPENAI_AVAILABLE:
            logger.warning(
                "OpenAI package not installed. Install it with 'pip install openai>=1.0.0'"
            )
            return

        self.client = self._initialize_client()
        self._models = {
            "text-embedding-ada-002": {
                "dimensions": 1536,
                "input_types": ["text"],
            },
            "text-embedding-3-small": {
                "dimensions": 1536,
                "input_types": ["text"],
            },
            "text-embedding-3-large": {
                "dimensions": 3072,
                "input_types": ["text"],
            },
        }

    def _initialize_client(self) -> Optional[OpenAI]:
        """Initialize the OpenAI client.

        Returns:
            The OpenAI client instance.

        Raises:
            AuthenticationError: If the API key is not provided.
        """
        if not OPENAI_AVAILABLE:
            return None

        api_key = self.config.get("api_key")
        if not api_key:
            api_key = openai.api_key

        if not api_key:
            logger.warning("OpenAI API key not provided")
            return None

        client_kwargs = {"api_key": api_key}
        
        organization = self.config.get("organization")
        if organization:
            client_kwargs["organization"] = organization

        return OpenAI(**client_kwargs)

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
            ProviderError: If there's an error from the OpenAI API.
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. Install it with 'pip install openai>=1.0.0'"
            )

        if not self.client:
            raise AuthenticationError("OpenAI client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            response = self.client.embeddings.create(
                input=input_data,
                model=model_name,
                **kwargs
            )
            return cast(List[float], response.data[0].embedding)
        except openai.RateLimitError as e:
            raise RateLimitError(f"OpenAI rate limit exceeded: {str(e)}")
        except openai.AuthenticationError as e:
            raise AuthenticationError(f"OpenAI authentication error: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Error creating embedding with OpenAI: {str(e)}")

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
            ProviderError: If there's an error from the OpenAI API.
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. Install it with 'pip install openai>=1.0.0'"
            )

        if not self.client:
            raise AuthenticationError("OpenAI client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            response = self.client.embeddings.create(
                input=inputs,
                model=model_name,
                **kwargs
            )
            
            # Sort embeddings by index to ensure correct order
            sorted_data = sorted(response.data, key=lambda x: x.index)
            return [cast(List[float], item.embedding) for item in sorted_data]
        except openai.RateLimitError as e:
            raise RateLimitError(f"OpenAI rate limit exceeded: {str(e)}")
        except openai.AuthenticationError as e:
            raise AuthenticationError(f"OpenAI authentication error: {str(e)}")
        except Exception as e:
            raise ProviderError(f"Error creating embeddings with OpenAI: {str(e)}")