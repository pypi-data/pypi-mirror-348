"""Base provider interface for embedding models."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

InputType = Union[str, List[str], Dict[str, Any]]
EmbeddingType = List[float]


class Provider(ABC):
    """Base class for embedding providers."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the provider.

        Args:
            config: Provider-specific configuration.
        """
        self.config = config or {}

    @abstractmethod
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
        """
        pass

    @abstractmethod
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
        """
        pass

    @abstractmethod
    def supports_model(self, model_name: str) -> bool:
        """Check if this provider supports the given model.

        Args:
            model_name: The name of the model to check.

        Returns:
            True if the provider supports the model, False otherwise.
        """
        pass

    @abstractmethod
    def supported_models(self) -> List[str]:
        """Get the list of models supported by this provider.

        Returns:
            List of supported model names.
        """
        pass

    @abstractmethod
    def supported_input_types(self) -> List[str]:
        """Get the list of input types supported by this provider.

        Returns:
            List of supported input types.
        """
        pass