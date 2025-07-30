Providers
=========

This page provides information about the embedding providers supported by OpenEmbed.

OpenAI
-----

OpenEmbed supports OpenAI's embedding models through the OpenAI API.

Supported Models
~~~~~~~~~~~~~~

- ``text-embedding-ada-002``: 1536-dimensional embeddings
- ``text-embedding-3-small``: 1536-dimensional embeddings
- ``text-embedding-3-large``: 3072-dimensional embeddings

Configuration
~~~~~~~~~~~

You can configure the OpenAI provider using the following methods:

Environment Variables:

.. code-block:: bash

    export OPENAI_API_KEY=sk-...
    export OPENAI_ORGANIZATION=org-...  # Optional

Direct Configuration:

.. code-block:: python

    client = EmbeddingClient(
        provider_config={
            "openai": {
                "api_key": "sk-...",
                "organization": "org-..."  # Optional
            }
        }
    )

Usage Example:

.. code-block:: python

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="text-embedding-ada-002"
    )

Cohere
------

OpenEmbed supports Cohere's embedding models through the Cohere API.

Supported Models
~~~~~~~~~~~~~~

- ``embed-english-v2.0``: 4096-dimensional embeddings
- ``embed-english-light-v2.0``: 1024-dimensional embeddings
- ``embed-multilingual-v2.0``: 768-dimensional embeddings

Configuration
~~~~~~~~~~~

You can configure the Cohere provider using the following methods:

Environment Variables:

.. code-block:: bash

    export COHERE_API_KEY=...

Direct Configuration:

.. code-block:: python

    client = EmbeddingClient(
        provider_config={
            "cohere": {
                "api_key": "..."
            }
        }
    )

Usage Example:

.. code-block:: python

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="embed-english-v2.0"
    )

Hugging Face
-----------

OpenEmbed supports Hugging Face's embedding models through the Transformers library.

Supported Models
~~~~~~~~~~~~~~

- ``sentence-transformers/all-MiniLM-L6-v2``: 384-dimensional embeddings
- ``sentence-transformers/all-mpnet-base-v2``: 768-dimensional embeddings
- ``sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2``: 384-dimensional embeddings

Additionally, any model from the Sentence Transformers library can be used by specifying its full path.

Configuration
~~~~~~~~~~~

You can configure the Hugging Face provider using the following methods:

Environment Variables:

.. code-block:: bash

    export HUGGINGFACE_API_KEY=...  # Optional, for accessing gated models

Direct Configuration:

.. code-block:: python

    client = EmbeddingClient(
        provider_config={
            "huggingface": {
                "api_key": "...",  # Optional, for accessing gated models
                "cache_dir": "..."  # Optional, for caching models
            }
        }
    )

Usage Example:

.. code-block:: python

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

Voyage AI
--------

OpenEmbed supports Voyage AI's embedding models through the Voyage AI API.

Supported Models
~~~~~~~~~~~~~~

- ``voyage-large-2``: 1024-dimensional embeddings
- ``voyage-code-2``: 1024-dimensional embeddings
- ``voyage-large-2-instruct``: 1024-dimensional embeddings

Configuration
~~~~~~~~~~~

You can configure the Voyage AI provider using the following methods:

Environment Variables:

.. code-block:: bash

    export VOYAGEAI_API_KEY=...

Direct Configuration:

.. code-block:: python

    client = EmbeddingClient(
        provider_config={
            "voyageai": {
                "api_key": "..."
            }
        }
    )

Usage Example:

.. code-block:: python

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="voyage-large-2"
    )

Amazon Titan
-----------

OpenEmbed supports Amazon Titan embedding models through Amazon Bedrock.

Supported Models
~~~~~~~~~~~~~~

- ``amazon.titan-embed-text-v1``: 1536-dimensional embeddings
- ``amazon.titan-embed-image-v1``: 1024-dimensional embeddings (for images)

Configuration
~~~~~~~~~~~

You can configure the Amazon Titan provider using the following methods:

Environment Variables:

.. code-block:: bash

    export AWS_ACCESS_KEY_ID=...
    export AWS_SECRET_ACCESS_KEY=...
    export AWS_REGION=us-west-2  # Default: us-west-2

Direct Configuration:

.. code-block:: python

    client = EmbeddingClient(
        provider_config={
            "amazon": {
                "aws_access_key_id": "...",
                "aws_secret_access_key": "...",
                "region_name": "us-west-2"  # Default: us-west-2
            }
        }
    )

Usage Example:

.. code-block:: python

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="amazon.titan-embed-text-v1"
    )

Custom Providers
--------------

You can create and register custom providers to support additional embedding models.

Creating a Custom Provider
~~~~~~~~~~~~~~~~~~~~~~~~

To create a custom provider, subclass the ``Provider`` class and implement its methods:

.. code-block:: python

    from openembed.providers.base import Provider

    class CustomProvider(Provider):
        def __init__(self, config=None):
            super().__init__(config)
            # Initialize your provider

        def create_embedding(self, input_data, model_name, **kwargs):
            # Implement embedding creation
            return [...]  # Return the embedding vector

        def batch_create_embeddings(self, inputs, model_name, **kwargs):
            # Implement batch embedding creation
            return [...]  # Return a list of embedding vectors

        def supports_model(self, model_name):
            # Check if the provider supports the model
            return model_name == "custom-model"

        def supported_models(self):
            # Return a list of supported models
            return ["custom-model"]

        def supported_input_types(self):
            # Return a list of supported input types
            return ["text"]

Registering a Custom Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register your custom provider with the client:

.. code-block:: python

    client = EmbeddingClient()
    client.register_provider("custom", CustomProvider())

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="custom-model"
    )