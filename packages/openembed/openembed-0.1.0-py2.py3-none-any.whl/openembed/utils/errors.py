"""Error definitions for the OpenEmbed library."""


class OpenEmbedError(Exception):
    """Base class for all OpenEmbed errors."""

    pass


class ProviderError(OpenEmbedError):
    """Error from an embedding provider."""

    pass


class ModelNotFoundError(ProviderError):
    """Error when a model is not found or not supported."""

    pass


class AuthenticationError(ProviderError):
    """Error when authentication fails."""

    pass


class RateLimitError(ProviderError):
    """Error when a rate limit is exceeded."""

    pass


class InputProcessingError(OpenEmbedError):
    """Error when processing input data."""

    pass


class CacheError(OpenEmbedError):
    """Error when using the cache."""

    pass