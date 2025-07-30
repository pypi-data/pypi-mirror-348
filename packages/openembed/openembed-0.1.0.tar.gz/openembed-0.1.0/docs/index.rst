OpenEmbed Documentation
======================

OpenEmbed is a unified interface for vector embeddings from different providers.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   providers
   advanced

Features
--------

- Single API for multiple embedding providers (OpenAI, Cohere, Hugging Face, Voyage AI, Amazon Titan)
- Support for different input types (text, with extensibility for images)
- Caching mechanism to avoid redundant API calls
- Batching support for efficient processing
- Extensible architecture for adding new providers and input types

Installation
-----------

You can install OpenEmbed using pip:

.. code-block:: bash

   pip install openembed

To install with specific provider dependencies:

.. code-block:: bash

   pip install openembed[openai]     # For OpenAI support
   pip install openembed[cohere]     # For Cohere support
   pip install openembed[huggingface] # For Hugging Face support
   pip install openembed[voyageai]   # For Voyage AI support
   pip install openembed[amazon]     # For Amazon Titan support
   pip install openembed[all]        # For all providers

Quick Start
----------

.. code-block:: python

   from openembed import EmbeddingClient

   # Initialize the client
   client = EmbeddingClient()

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`