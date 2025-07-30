"""HuggingFace provider for embedding models."""

import logging
import os
from typing import Any, Dict, List, Optional, Union, cast

try:
    import torch
    import transformers
    from transformers import AutoTokenizer, AutoModel
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False

import numpy as np

from openembed.providers.base import Provider, InputType, EmbeddingType
from openembed.utils.errors import (
    ProviderError,
    ModelNotFoundError,
    AuthenticationError,
)

logger = logging.getLogger(__name__)


class HuggingFaceProvider(Provider):
    """Provider for HuggingFace embedding models."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the HuggingFace provider.

        Args:
            config: Configuration for the HuggingFace API.
                Example: {"api_key": "...", "cache_dir": "..."}
        """
        super().__init__(config)
        
        if not HUGGINGFACE_AVAILABLE:
            logger.warning(
                "HuggingFace transformers package not installed. "
                "Install it with 'pip install transformers torch'"
            )
            return

        self.api_key = self.config.get("api_key")
        if self.api_key:
            os.environ["HUGGINGFACE_TOKEN"] = self.api_key

        self.cache_dir = self.config.get("cache_dir")
        
        # Dictionary to cache loaded models and tokenizers
        self.loaded_models: Dict[str, Any] = {}
        
        self._models = {
            "sentence-transformers/all-MiniLM-L6-v2": {
                "dimensions": 384,
                "input_types": ["text"],
            },
            "sentence-transformers/all-mpnet-base-v2": {
                "dimensions": 768,
                "input_types": ["text"],
            },
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": {
                "dimensions": 384,
                "input_types": ["text"],
            },
        }

    def _load_model(self, model_name: str) -> tuple:
        """Load a model and tokenizer from HuggingFace.

        Args:
            model_name: The name of the model to load.

        Returns:
            Tuple of (tokenizer, model).

        Raises:
            ModelNotFoundError: If the model cannot be loaded.
        """
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        try:
            kwargs = {}
            if self.cache_dir:
                kwargs["cache_dir"] = self.cache_dir

            tokenizer = AutoTokenizer.from_pretrained(model_name, **kwargs)
            model = AutoModel.from_pretrained(model_name, **kwargs)
            
            # Move model to GPU if available
            if torch.cuda.is_available():
                model = model.to("cuda")
            
            self.loaded_models[model_name] = (tokenizer, model)
            return tokenizer, model
        except Exception as e:
            raise ModelNotFoundError(f"Error loading model {model_name}: {str(e)}")

    def supports_model(self, model_name: str) -> bool:
        """Check if this provider supports the given model.

        Args:
            model_name: The name of the model to check.

        Returns:
            True if the provider supports the model, False otherwise.
        """
        # Check our predefined models
        if model_name in self._models:
            return True
        
        # Also allow any sentence-transformers model
        return model_name.startswith("sentence-transformers/")

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

    def _mean_pooling(self, model_output, attention_mask):
        """Perform mean pooling on model output using attention mask.
        
        Args:
            model_output: The output from the model.
            attention_mask: The attention mask from the tokenizer.
            
        Returns:
            The pooled embeddings.
        """
        # First element of model_output contains all token embeddings
        token_embeddings = model_output[0]
        
        # Expand attention mask from [batch_size, seq_length] to [batch_size, seq_length, hidden_size]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        
        # Sum token embeddings and divide by the expanded mask
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        # Return mean pooled embeddings
        return sum_embeddings / sum_mask

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
            ProviderError: If there's an error from the HuggingFace API.
        """
        if not HUGGINGFACE_AVAILABLE:
            raise ImportError(
                "HuggingFace transformers package not installed. "
                "Install it with 'pip install transformers torch'"
            )

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            tokenizer, model = self._load_model(model_name)
            
            # Tokenize the input
            encoded_input = tokenizer(
                input_data,
                padding=True,
                truncation=True,
                return_tensors="pt",
                max_length=kwargs.get("max_length", 512),
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                encoded_input = {k: v.to("cuda") for k, v in encoded_input.items()}
            
            # Compute token embeddings
            with torch.no_grad():
                model_output = model(**encoded_input)
            
            # Perform pooling
            embeddings = self._mean_pooling(model_output, encoded_input["attention_mask"])
            
            # Normalize embeddings
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            # Convert to numpy and then to list
            embedding_np = embeddings[0].cpu().numpy()
            return embedding_np.tolist()
        except Exception as e:
            raise ProviderError(f"Error creating embedding with HuggingFace: {str(e)}")

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
            ProviderError: If there's an error from the HuggingFace API.
        """
        if not HUGGINGFACE_AVAILABLE:
            raise ImportError(
                "HuggingFace transformers package not installed. "
                "Install it with 'pip install transformers torch'"
            )

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        try:
            tokenizer, model = self._load_model(model_name)
            
            # Tokenize the inputs
            encoded_inputs = tokenizer(
                inputs,
                padding=True,
                truncation=True,
                return_tensors="pt",
                max_length=kwargs.get("max_length", 512),
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                encoded_inputs = {k: v.to("cuda") for k, v in encoded_inputs.items()}
            
            # Compute token embeddings
            with torch.no_grad():
                model_output = model(**encoded_inputs)
            
            # Perform pooling
            embeddings = self._mean_pooling(model_output, encoded_inputs["attention_mask"])
            
            # Normalize embeddings
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            # Convert to numpy and then to list
            embeddings_np = embeddings.cpu().numpy()
            return [embedding.tolist() for embedding in embeddings_np]
        except Exception as e:
            raise ProviderError(f"Error creating embeddings with HuggingFace: {str(e)}")