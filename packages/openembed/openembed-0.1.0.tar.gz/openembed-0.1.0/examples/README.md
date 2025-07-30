# OpenEmbed Examples

This directory contains examples of how to use the OpenEmbed library.

## Basic Usage

The `basic_usage.py` script demonstrates the basic functionality of the OpenEmbed library:

- Creating embeddings with different providers
- Batch processing
- Caching

To run the example:

```bash
python basic_usage.py
```

## Setting Up API Keys

Before running the examples, you need to set up API keys for the providers you want to use:

### OpenAI

```bash
export OPENAI_API_KEY=sk-...
```

### Cohere

```bash
export COHERE_API_KEY=...
```

### Hugging Face

```bash
export HUGGINGFACE_API_KEY=...
```

### Voyage AI

```bash
export VOYAGEAI_API_KEY=...
```

### Amazon Titan

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-west-2
```

## Additional Examples

More examples will be added in the future, including:

- Similarity search
- Dimension reduction
- Integration with vector databases
- Custom providers
- Advanced caching strategies