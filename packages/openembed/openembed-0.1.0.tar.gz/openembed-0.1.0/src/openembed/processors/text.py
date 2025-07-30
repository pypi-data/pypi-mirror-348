"""Text input processor."""

import logging
import re
from typing import Any, Dict, List, Optional, Union

from openembed.processors.base import InputProcessor, InputType, ProcessedType
from openembed.utils.errors import InputProcessingError

logger = logging.getLogger(__name__)


class TextProcessor(InputProcessor):
    """Processor for text inputs."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the text processor.

        Args:
            config: Configuration for the text processor.
                Example: {
                    "max_length": 8192,
                    "truncation_strategy": "end",  # "start", "end", or "middle"
                    "clean_text": True,
                    "lowercase": False,
                    "strip_whitespace": True,
                    "strip_html": True,
                }
        """
        super().__init__(config)
        self.max_length = self.config.get("max_length", 8192)
        self.truncation_strategy = self.config.get("truncation_strategy", "end")
        self.clean_text = self.config.get("clean_text", True)
        self.lowercase = self.config.get("lowercase", False)
        self.strip_whitespace = self.config.get("strip_whitespace", True)
        self.strip_html = self.config.get("strip_html", True)

    def supported_input_types(self) -> List[str]:
        """Get the list of input types supported by this processor.

        Returns:
            List of supported input types.
        """
        return ["text"]

    def _clean_text_content(self, text: str) -> str:
        """Clean the text content.

        Args:
            text: The text to clean.

        Returns:
            The cleaned text.
        """
        if not self.clean_text:
            return text

        # Convert to lowercase if configured
        if self.lowercase:
            text = text.lower()

        # Strip HTML tags if configured
        if self.strip_html:
            text = re.sub(r"<[^>]*>", "", text)

        # Strip excessive whitespace if configured
        if self.strip_whitespace:
            text = re.sub(r"\s+", " ", text)
            text = text.strip()

        return text

    def _truncate_text(self, text: str) -> str:
        """Truncate the text to the maximum length.

        Args:
            text: The text to truncate.

        Returns:
            The truncated text.
        """
        if len(text) <= self.max_length:
            return text

        if self.truncation_strategy == "start":
            return text[-self.max_length:]
        elif self.truncation_strategy == "end":
            return text[:self.max_length]
        elif self.truncation_strategy == "middle":
            half_length = self.max_length // 2
            return text[:half_length] + text[-half_length:]
        else:
            logger.warning(f"Unknown truncation strategy: {self.truncation_strategy}. Using 'end'.")
            return text[:self.max_length]

    def process_single_text(self, text: str) -> str:
        """Process a single text input.

        Args:
            text: The text to process.

        Returns:
            The processed text.
        """
        if not isinstance(text, str):
            text = str(text)

        # Clean the text
        text = self._clean_text_content(text)

        # Truncate the text
        text = self._truncate_text(text)

        return text

    def process(self, input_data: InputType) -> ProcessedType:
        """Process the input data.

        Args:
            input_data: The input data to process.

        Returns:
            The processed input data.

        Raises:
            InputProcessingError: If the input data cannot be processed.
        """
        try:
            if isinstance(input_data, str):
                return self.process_single_text(input_data)
            elif isinstance(input_data, list):
                return [self.process_single_text(item) for item in input_data]
            elif isinstance(input_data, dict):
                # Process each value in the dictionary
                return {key: self.process_single_text(value) if isinstance(value, str) else value
                        for key, value in input_data.items()}
            else:
                raise InputProcessingError(f"Unsupported input type: {type(input_data)}")
        except Exception as e:
            raise InputProcessingError(f"Error processing text input: {str(e)}")