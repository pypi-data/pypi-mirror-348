Usage
=====

This page provides examples of how to use the OpenEmbed library.

Basic Usage
----------

Creating a client
~~~~~~~~~~~~~~~~

To use OpenEmbed, first create an ``EmbeddingClient`` instance:

.. code-block:: python

    from openembed import EmbeddingClient

    # Initialize the client
    client = EmbeddingClient()

Creating embeddings
~~~~~~~~~~~~~~~~~~

You can create embeddings using different models from various providers:

.. code-block:: python

    # Create an embedding using OpenAI
    embedding = client.create_embedding(
        "This is a sample text",
        model_name="text-embedding-ada-002"
    )

    # Create an embedding using Cohere
    embedding = client.create_embedding(
        "This is a sample text",
        model_name="embed-english-v2.0"
    )

    # Create an embedding using Hugging Face
    embedding = client.create_embedding(
        "This is a sample text",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create an embedding using Voyage AI
    embedding = client.create_embedding(
        "This is a sample text",
        model_name="voyage-large-2"
    )

    # Create an embedding using Amazon Titan
    embedding = client.create_embedding(
        "This is a sample text",
        model_name="amazon.titan-embed-text-v1"
    )

Batch Processing
---------------

You can create embeddings for multiple inputs in a batch:

.. code-block:: python

    texts = [
        "This is the first document",
        "This is the second document",
        "And this is the third one"
    ]

    embeddings = client.batch_create_embeddings(
        texts,
        model_name="text-embedding-ada-002",
        batch_size=10
    )

Configuration
------------

Provider configuration
~~~~~~~~~~~~~~~~~~~~~

You can configure providers when initializing the client:

.. code-block:: python

    client = EmbeddingClient(
        provider_config={
            "openai": {
                "api_key": "sk-...",
                "organization": "org-..."
            },
            "cohere": {
                "api_key": "..."
            },
            "voyageai": {
                "api_key": "..."
            },
            "amazon": {
                "aws_access_key_id": "...",
                "aws_secret_access_key": "...",
                "region_name": "us-west-2"
            }
        }
    )

Environment variables
~~~~~~~~~~~~~~~~~~~~

You can also configure providers using environment variables:

.. code-block:: bash

    # OpenAI
    export OPENAI_API_KEY=sk-...

    # Cohere
    export COHERE_API_KEY=...

    # Hugging Face
    export HUGGINGFACE_API_KEY=...

    # Voyage AI
    export VOYAGEAI_API_KEY=...

    # Amazon
    export AWS_ACCESS_KEY_ID=...
    export AWS_SECRET_ACCESS_KEY=...
    export AWS_REGION=us-west-2

Caching
-------

Enabling caching
~~~~~~~~~~~~~~~

You can enable caching to avoid redundant API calls:

.. code-block:: python

    # Enable in-memory caching
    client = EmbeddingClient(cache_enabled=True)

    # Enable disk-based caching
    client = EmbeddingClient(
        cache_enabled=True,
        cache_dir="./cache"
    )

Disabling caching for specific calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can disable caching for specific calls:

.. code-block:: python

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="text-embedding-ada-002",
        use_cache=False
    )

Clearing the cache
~~~~~~~~~~~~~~~~

You can clear the cache:

.. code-block:: python

    client.clear_cache()

Advanced Usage
-------------

Custom providers
~~~~~~~~~~~~~~

You can register custom providers:

.. code-block:: python

    from openembed.providers.base import Provider

    class CustomProvider(Provider):
        # Implement the provider interface
        ...

    client = EmbeddingClient()
    client.register_provider("custom", CustomProvider())

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="custom-model"
    )

Error handling
~~~~~~~~~~~~

You can handle errors from the library:

.. code-block:: python

    from openembed.utils.errors import (
        OpenEmbedError,
        ProviderError,
        ModelNotFoundError,
        AuthenticationError,
        RateLimitError,
    )

    try:
        embedding = client.create_embedding(
            "This is a sample text",
            model_name="invalid-model"
        )
    except ModelNotFoundError as e:
        print(f"Model not found: {e}")
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
    except ProviderError as e:
        print(f"Provider error: {e}")
    except OpenEmbedError as e:
        print(f"OpenEmbed error: {e}")