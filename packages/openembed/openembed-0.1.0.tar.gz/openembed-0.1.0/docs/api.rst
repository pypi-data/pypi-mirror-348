API Reference
=============

This page provides detailed documentation for the OpenEmbed API.

EmbeddingClient
--------------

.. code-block:: python

    from openembed import EmbeddingClient

The ``EmbeddingClient`` is the main entry point for the OpenEmbed library.

.. py:class:: EmbeddingClient(provider_config=None, cache_enabled=True, cache_dir=None)

    Initialize the embedding client.

    :param provider_config: Configuration for different providers.
        Example: ``{"openai": {"api_key": "sk-..."}}``
    :type provider_config: dict, optional
    :param cache_enabled: Whether to enable caching.
    :type cache_enabled: bool
    :param cache_dir: Directory to store cache files.
    :type cache_dir: str, optional

    .. py:method:: create_embedding(input_data, model_name, use_cache=True, **kwargs)

        Create an embedding for the given input.

        :param input_data: The input to create an embedding for (text, image path, etc.).
        :type input_data: str, list, or dict
        :param model_name: The name of the model to use.
        :type model_name: str
        :param use_cache: Whether to use the cache.
        :type use_cache: bool
        :param kwargs: Additional model-specific parameters.
        :return: The embedding vector.
        :rtype: list
        :raises ModelNotFoundError: If no provider supports the model.
        :raises ProviderError: If there's an error from the provider.

    .. py:method:: batch_create_embeddings(inputs, model_name, batch_size=32, use_cache=True, **kwargs)

        Create embeddings for multiple inputs in a batch.

        :param inputs: List of inputs to create embeddings for.
        :type inputs: list
        :param model_name: The name of the model to use.
        :type model_name: str
        :param batch_size: The batch size to use.
        :type batch_size: int
        :param use_cache: Whether to use the cache.
        :type use_cache: bool
        :param kwargs: Additional model-specific parameters.
        :return: List of embedding vectors.
        :rtype: list
        :raises ModelNotFoundError: If no provider supports the model.
        :raises ProviderError: If there's an error from the provider.

    .. py:method:: register_provider(name, provider)

        Register a provider.

        :param name: The name of the provider.
        :type name: str
        :param provider: The provider instance.
        :type provider: Provider

    .. py:method:: register_processor(name, processor)

        Register an input processor.

        :param name: The name of the processor.
        :type name: str
        :param processor: The processor instance.
        :type processor: InputProcessor

    .. py:method:: clear_cache()

        Clear the cache.

Provider Interface
----------------

.. code-block:: python

    from openembed.providers.base import Provider

The ``Provider`` class is the base class for all provider implementations.

.. py:class:: Provider(config=None)

    Base class for embedding providers.

    :param config: Provider-specific configuration.
    :type config: dict, optional

    .. py:method:: create_embedding(input_data, model_name, **kwargs)

        Create an embedding for the given input.

        :param input_data: The processed input to create an embedding for.
        :type input_data: str, list, or dict
        :param model_name: The name of the model to use.
        :type model_name: str
        :param kwargs: Additional model-specific parameters.
        :return: The embedding vector.
        :rtype: list

    .. py:method:: batch_create_embeddings(inputs, model_name, **kwargs)

        Create embeddings for multiple inputs in a batch.

        :param inputs: List of processed inputs to create embeddings for.
        :type inputs: list
        :param model_name: The name of the model to use.
        :type model_name: str
        :param kwargs: Additional model-specific parameters.
        :return: List of embedding vectors.
        :rtype: list

    .. py:method:: supports_model(model_name)

        Check if this provider supports the given model.

        :param model_name: The name of the model to check.
        :type model_name: str
        :return: True if the provider supports the model, False otherwise.
        :rtype: bool

    .. py:method:: supported_models()

        Get the list of models supported by this provider.

        :return: List of supported model names.
        :rtype: list

    .. py:method:: supported_input_types()

        Get the list of input types supported by this provider.

        :return: List of supported input types.
        :rtype: list

InputProcessor Interface
----------------------

.. code-block:: python

    from openembed.processors.base import InputProcessor

The ``InputProcessor`` class is the base class for all input processor implementations.

.. py:class:: InputProcessor(config=None)

    Base class for input processors.

    :param config: Processor-specific configuration.
    :type config: dict, optional

    .. py:method:: process(input_data)

        Process the input data.

        :param input_data: The input data to process.
        :type input_data: str, list, or dict
        :return: The processed input data.
        :rtype: str, list, or dict

    .. py:method:: supported_input_types()

        Get the list of input types supported by this processor.

        :return: List of supported input types.
        :rtype: list

CacheManager Interface
--------------------

.. code-block:: python

    from openembed.cache.base import CacheManager

The ``CacheManager`` class is the base class for all cache manager implementations.

.. py:class:: CacheManager(config=None)

    Base class for cache managers.

    :param config: Cache-specific configuration.
    :type config: dict, optional

    .. py:method:: get(key)

        Get a value from the cache.

        :param key: The cache key.
        :type key: str
        :return: The cached value, or None if the key is not in the cache.
        :rtype: any

    .. py:method:: set(key, value)

        Set a value in the cache.

        :param key: The cache key.
        :type key: str
        :param value: The value to cache.
        :type value: any

    .. py:method:: delete(key)

        Delete a value from the cache.

        :param key: The cache key.
        :type key: str

    .. py:method:: clear()

        Clear the cache.

    .. py:method:: contains(key)

        Check if a key is in the cache.

        :param key: The cache key.
        :type key: str
        :return: True if the key is in the cache, False otherwise.
        :rtype: bool

Error Classes
-----------

.. code-block:: python

    from openembed.utils.errors import (
        OpenEmbedError,
        ProviderError,
        ModelNotFoundError,
        AuthenticationError,
        RateLimitError,
        InputProcessingError,
    )

The library defines several error classes:

.. py:class:: OpenEmbedError

    Base class for all OpenEmbed errors.

.. py:class:: ProviderError

    Error from an embedding provider.

.. py:class:: ModelNotFoundError

    Error when a model is not found or not supported.

.. py:class:: AuthenticationError

    Error when authentication fails.

.. py:class:: RateLimitError

    Error when a rate limit is exceeded.

.. py:class:: InputProcessingError

    Error when processing input data.

.. py:class:: CacheError

    Error when using the cache.