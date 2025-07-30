"""Base input processor interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

InputType = Union[str, List[str], Dict[str, Any]]
ProcessedType = Union[str, List[str], Dict[str, Any]]


class InputProcessor(ABC):
    """Base class for input processors."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the input processor.

        Args:
            config: Processor-specific configuration.
        """
        self.config = config or {}

    @abstractmethod
    def process(self, input_data: InputType) -> ProcessedType:
        """Process the input data.

        Args:
            input_data: The input data to process.

        Returns:
            The processed input data.
        """
        pass

    @abstractmethod
    def supported_input_types(self) -> List[str]:
        """Get the list of input types supported by this processor.

        Returns:
            List of supported input types.
        """
        pass