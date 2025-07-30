Installation
============

This page provides instructions for installing the OpenEmbed library.

Requirements
-----------

OpenEmbed requires Python 3.8 or later.

Basic Installation
----------------

You can install OpenEmbed using pip:

.. code-block:: bash

    pip install openembed

This will install the core library without any provider-specific dependencies.

Provider-Specific Installation
----------------------------

To use specific embedding providers, you can install the corresponding dependencies:

OpenAI
~~~~~~

.. code-block:: bash

    pip install openembed[openai]

This will install the OpenAI Python client library.

Cohere
~~~~~~

.. code-block:: bash

    pip install openembed[cohere]

This will install the Cohere Python client library.

Hugging Face
~~~~~~~~~~~

.. code-block:: bash

    pip install openembed[huggingface]

This will install the Transformers library and PyTorch.

Voyage AI
~~~~~~~~

.. code-block:: bash

    pip install openembed[voyageai]

This will install the Voyage AI Python client library.

Amazon Titan
~~~~~~~~~~~

.. code-block:: bash

    pip install openembed[amazon]

This will install the boto3 library for AWS services.

All Providers
~~~~~~~~~~~~

To install dependencies for all supported providers:

.. code-block:: bash

    pip install openembed[all]

Development Installation
----------------------

For development, you can install the library with development dependencies:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/username/openembed.git
    cd openembed

    # Create a virtual environment (optional but recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install development dependencies
    pip install -e ".[dev,all]"

This will install the library in development mode along with all provider dependencies and development tools like pytest, black, flake8, etc.

Verifying Installation
--------------------

You can verify that OpenEmbed is installed correctly by running:

.. code-block:: python

    import openembed
    print(openembed.__version__)

This should print the version number of the installed library.