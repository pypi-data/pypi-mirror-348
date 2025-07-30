# OpenEmbed

[![PyPI version](https://img.shields.io/pypi/v/openembed.svg)](https://pypi.org/project/openembed/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/openembed.svg)](https://pypi.org/project/openembed/)

A unified interface for vector embeddings from different providers.

## Features

- Single API for multiple embedding providers (OpenAI, Cohere, Hugging Face, Voyage AI, Amazon Titan)
- Support for different input types (text, with extensibility for images)
- Caching mechanism to avoid redundant API calls
- Batching support for efficient processing
- Extensible architecture for adding new providers and input types

## Installation

```bash
pip install openembed
```

To install with specific provider dependencies:

```bash
pip install openembed[openai]     # For OpenAI support
pip install openembed[cohere]     # For Cohere support
pip install openembed[huggingface] # For Hugging Face support
pip install openembed[voyageai]   # For Voyage AI support
pip install openembed[amazon]     # For Amazon Titan support
pip install openembed[all]        # For all providers
```

## Usage

### Basic Usage

```python
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
```

### Batch Processing

```python
from openembed import EmbeddingClient

client = EmbeddingClient()

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
```

### Custom Configuration

```python
from openembed import EmbeddingClient

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
    },
    cache_enabled=True,
    cache_dir="./cache"
)
```

## Development

### Setup development environment

```bash
# Clone the repository
git clone https://github.com/username/openembed.git
cd openembed

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev,all]"
```

### Run tests

```bash
pytest
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.