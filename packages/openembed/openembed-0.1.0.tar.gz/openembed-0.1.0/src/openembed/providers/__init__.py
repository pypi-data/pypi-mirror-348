"""Provider implementations for different embedding services."""

from openembed.providers.base import Provider
from openembed.providers.openai import OpenAIProvider
from openembed.providers.cohere import CohereProvider
from openembed.providers.huggingface import HuggingFaceProvider
from openembed.providers.voyageai import VoyageAIProvider
from openembed.providers.amazon import AmazonTitanProvider

__all__ = [
    "Provider",
    "OpenAIProvider",
    "CohereProvider",
    "HuggingFaceProvider",
    "VoyageAIProvider",
    "AmazonTitanProvider",
]