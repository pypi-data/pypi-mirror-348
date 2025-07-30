"""Configuration utilities for the OpenEmbed library."""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATHS = [
    "~/.openembed/config.json",
    "~/.config/openembed/config.json",
    "./.openembed.json",
]


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from a file.

    Args:
        config_path: Path to the configuration file. If None, default paths will be checked.

    Returns:
        The configuration dictionary.
    """
    # Check environment variable for config path
    if config_path is None:
        config_path = os.environ.get("OPENEMBED_CONFIG")

    # If config_path is provided or found in environment, try to load it
    if config_path:
        config_path = os.path.expanduser(config_path)
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error loading config from {config_path}: {str(e)}")
        else:
            logger.warning(f"Config file not found: {config_path}")

    # Try default paths
    for path in DEFAULT_CONFIG_PATHS:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            try:
                with open(expanded_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error loading config from {expanded_path}: {str(e)}")

    # No config found, return empty dict
    return {}


def save_config(config: Dict[str, Any], config_path: str) -> bool:
    """Save configuration to a file.

    Args:
        config: The configuration dictionary.
        config_path: Path to the configuration file.

    Returns:
        True if the configuration was saved successfully, False otherwise.
    """
    config_path = os.path.expanduser(config_path)
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(config_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logger.warning(f"Error saving config to {config_path}: {str(e)}")
        return False


def get_api_key(provider: str) -> Optional[str]:
    """Get an API key for a provider from environment variables.

    Args:
        provider: The name of the provider.

    Returns:
        The API key, or None if not found.
    """
    # Check provider-specific environment variables
    if provider.lower() == "openai":
        return os.environ.get("OPENAI_API_KEY")
    elif provider.lower() == "cohere":
        return os.environ.get("COHERE_API_KEY")
    elif provider.lower() == "huggingface":
        return os.environ.get("HUGGINGFACE_API_KEY")
    elif provider.lower() == "voyageai":
        return os.environ.get("VOYAGEAI_API_KEY")
    
    # Check generic environment variable
    return os.environ.get(f"{provider.upper()}_API_KEY")


def get_provider_config(provider: str) -> Dict[str, Any]:
    """Get configuration for a provider.

    Args:
        provider: The name of the provider.

    Returns:
        The provider configuration.
    """
    config = load_config()
    provider_config = config.get("providers", {}).get(provider, {})
    
    # Add API key from environment if not in config
    if "api_key" not in provider_config:
        api_key = get_api_key(provider)
        if api_key:
            provider_config["api_key"] = api_key
    
    return provider_config