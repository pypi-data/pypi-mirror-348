"""Input processors for different types of data."""

from openembed.processors.base import InputProcessor
from openembed.processors.text import TextProcessor

__all__ = [
    "InputProcessor",
    "TextProcessor",
]