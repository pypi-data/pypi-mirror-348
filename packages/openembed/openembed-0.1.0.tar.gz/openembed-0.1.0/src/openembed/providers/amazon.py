"""Amazon Titan provider for embedding models."""

import json
import logging
from typing import Any, Dict, List, Optional, Union, cast

try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

from openembed.providers.base import Provider, InputType, EmbeddingType
from openembed.utils.errors import (
    ProviderError,
    ModelNotFoundError,
    AuthenticationError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class AmazonTitanProvider(Provider):
    """Provider for Amazon Titan embedding models through Amazon Bedrock."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Amazon Titan provider.

        Args:
            config: Configuration for the Amazon Bedrock API.
                Example: {
                    "aws_access_key_id": "...",
                    "aws_secret_access_key": "...",
                    "region_name": "us-west-2"
                }
        """
        super().__init__(config)
        
        if not BOTO3_AVAILABLE:
            logger.warning(
                "boto3 package not installed. Install it with 'pip install boto3'"
            )
            return

        self.client = self._initialize_client()
        self._models = {
            "amazon.titan-embed-text-v1": {
                "dimensions": 1536,
                "input_types": ["text"],
                "model_id": "amazon.titan-embed-text-v1",
            },
            "amazon.titan-embed-image-v1": {
                "dimensions": 1024,
                "input_types": ["image"],
                "model_id": "amazon.titan-embed-image-v1",
            },
        }

    def _initialize_client(self) -> Optional[Any]:
        """Initialize the Amazon Bedrock client.

        Returns:
            The Amazon Bedrock client instance.

        Raises:
            AuthenticationError: If the AWS credentials are not provided.
        """
        if not BOTO3_AVAILABLE:
            return None

        aws_access_key_id = self.config.get("aws_access_key_id")
        aws_secret_access_key = self.config.get("aws_secret_access_key")
        region_name = self.config.get("region_name", "us-west-2")

        if not aws_access_key_id or not aws_secret_access_key:
            # Try to use default credentials
            try:
                return boto3.client("bedrock-runtime", region_name=region_name)
            except Exception as e:
                logger.warning(f"Failed to initialize Amazon Bedrock client with default credentials: {str(e)}")
                return None
        
        try:
            return boto3.client(
                "bedrock-runtime",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
            )
        except Exception as e:
            logger.warning(f"Failed to initialize Amazon Bedrock client: {str(e)}")
            return None

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
        return ["text", "image"]

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
            ProviderError: If there's an error from the Amazon Bedrock API.
        """
        if not BOTO3_AVAILABLE:
            raise ImportError(
                "boto3 package not installed. Install it with 'pip install boto3'"
            )

        if not self.client:
            raise AuthenticationError("Amazon Bedrock client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        model_info = self._models[model_name]
        model_id = model_info["model_id"]

        try:
            # Prepare the request body based on the model
            if "text" in model_info["input_types"]:
                body = {
                    "inputText": input_data if isinstance(input_data, str) else str(input_data)
                }
            elif "image" in model_info["input_types"]:
                # For image embedding, input_data should be a base64-encoded image
                body = {
                    "inputImage": input_data
                }
            else:
                raise ValueError(f"Unsupported input type for model {model_name}")

            # Add any additional parameters
            for key, value in kwargs.items():
                body[key] = value

            # Invoke the model
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            # Parse the response
            response_body = json.loads(response["body"].read())
            
            if "embedding" in response_body:
                return cast(List[float], response_body["embedding"])
            else:
                raise ProviderError(f"Unexpected response format from Amazon Bedrock: {response_body}")
        except Exception as e:
            if "AccessDenied" in str(e):
                raise AuthenticationError(f"Amazon Bedrock authentication error: {str(e)}")
            elif "ThrottlingException" in str(e):
                raise RateLimitError(f"Amazon Bedrock rate limit exceeded: {str(e)}")
            else:
                raise ProviderError(f"Error creating embedding with Amazon Bedrock: {str(e)}")

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
            ProviderError: If there's an error from the Amazon Bedrock API.
        """
        if not BOTO3_AVAILABLE:
            raise ImportError(
                "boto3 package not installed. Install it with 'pip install boto3'"
            )

        if not self.client:
            raise AuthenticationError("Amazon Bedrock client not initialized")

        if not self.supports_model(model_name):
            raise ModelNotFoundError(f"Model not supported: {model_name}")

        # Amazon Bedrock doesn't support batch embedding in a single API call,
        # so we'll process each input individually
        embeddings = []
        for input_data in inputs:
            embedding = self.create_embedding(input_data, model_name, **kwargs)
            embeddings.append(embedding)
        
        return embeddings