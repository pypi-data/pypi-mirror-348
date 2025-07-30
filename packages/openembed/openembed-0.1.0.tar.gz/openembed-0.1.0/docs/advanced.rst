Advanced Usage
==============

This page provides information about advanced usage of the OpenEmbed library.

Custom Providers
--------------

Creating a Custom Provider
~~~~~~~~~~~~~~~~~~~~~~~~

You can create custom providers to support additional embedding models or services. To create a custom provider, subclass the ``Provider`` class and implement its methods:

.. code-block:: python

    from openembed.providers.base import Provider

    class CustomProvider(Provider):
        def __init__(self, config=None):
            super().__init__(config)
            # Initialize your provider with configuration
            self.api_key = self.config.get("api_key")
            # Initialize any client libraries or connections
            self.client = self._initialize_client()
            # Define supported models
            self._models = {
                "custom-model": {
                    "dimensions": 512,
                    "input_types": ["text"],
                },
            }

        def _initialize_client(self):
            # Initialize any client libraries or connections
            # Return the client or None if initialization fails
            return SomeClient(api_key=self.api_key)

        def create_embedding(self, input_data, model_name, **kwargs):
            # Implement embedding creation
            # Call your embedding service
            response = self.client.embed(input_data, model=model_name, **kwargs)
            # Process the response and return the embedding vector
            return response.embedding

        def batch_create_embeddings(self, inputs, model_name, **kwargs):
            # Implement batch embedding creation
            # Call your embedding service with multiple inputs
            response = self.client.embed_batch(inputs, model=model_name, **kwargs)
            # Process the response and return a list of embedding vectors
            return response.embeddings

        def supports_model(self, model_name):
            # Check if the provider supports the model
            return model_name in self._models

        def supported_models(self):
            # Return a list of supported models
            return list(self._models.keys())

        def supported_input_types(self):
            # Return a list of supported input types
            return ["text"]

Registering a Custom Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register your custom provider with the client:

.. code-block:: python

    client = EmbeddingClient()
    client.register_provider("custom", CustomProvider(config={"api_key": "..."}))

    embedding = client.create_embedding(
        "This is a sample text",
        model_name="custom-model"
    )

Custom Input Processors
---------------------

Creating a Custom Input Processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create custom input processors to handle different types of input data. To create a custom input processor, subclass the ``InputProcessor`` class and implement its methods:

.. code-block:: python

    from openembed.processors.base import InputProcessor

    class CustomProcessor(InputProcessor):
        def __init__(self, config=None):
            super().__init__(config)
            # Initialize your processor with configuration
            self.max_length = self.config.get("max_length", 1000)

        def process(self, input_data):
            # Implement input processing
            # Process the input data and return the processed data
            if isinstance(input_data, str):
                # Process a single input
                return self._process_single(input_data)
            elif isinstance(input_data, list):
                # Process a list of inputs
                return [self._process_single(item) for item in input_data]
            else:
                # Handle other types of input
                raise ValueError(f"Unsupported input type: {type(input_data)}")

        def _process_single(self, text):
            # Process a single text input
            # Implement your processing logic here
            # For example, truncate the text to the maximum length
            if len(text) > self.max_length:
                return text[:self.max_length]
            return text

        def supported_input_types(self):
            # Return a list of supported input types
            return ["text"]

Registering a Custom Input Processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register your custom input processor with the client:

.. code-block:: python

    client = EmbeddingClient()
    client.register_processor("custom", CustomProcessor(config={"max_length": 500}))

Custom Caching
------------

Creating a Custom Cache Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create custom cache managers to implement different caching strategies. To create a custom cache manager, subclass the ``CacheManager`` class and implement its methods:

.. code-block:: python

    from openembed.cache.base import CacheManager

    class CustomCache(CacheManager):
        def __init__(self, config=None):
            super().__init__(config)
            # Initialize your cache with configuration
            self.ttl = self.config.get("ttl", 3600)  # Default TTL: 1 hour
            # Initialize your cache storage
            self.cache = {}

        def get(self, key):
            # Get a value from the cache
            if key not in self.cache:
                return None
            # Check if the value is expired
            if self._is_expired(key):
                self.delete(key)
                return None
            # Return the cached value
            return self.cache[key]["value"]

        def set(self, key, value):
            # Set a value in the cache
            self.cache[key] = {
                "value": value,
                "timestamp": time.time(),
            }

        def delete(self, key):
            # Delete a value from the cache
            if key in self.cache:
                del self.cache[key]

        def clear(self):
            # Clear the cache
            self.cache.clear()

        def contains(self, key):
            # Check if a key is in the cache
            if key not in self.cache:
                return False
            # Check if the value is expired
            if self._is_expired(key):
                self.delete(key)
                return False
            return True

        def _is_expired(self, key):
            # Check if a cache entry is expired
            if self.ttl is None:
                return False
            entry = self.cache.get(key)
            if entry is None:
                return True
            return time.time() - entry["timestamp"] > self.ttl

Using a Custom Cache Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use your custom cache manager with the client:

.. code-block:: python

    client = EmbeddingClient()
    client.cache_manager = CustomCache(config={"ttl": 7200})  # 2 hours TTL

Dimension Reduction
-----------------

You can reduce the dimensionality of embeddings for more efficient storage and retrieval:

.. code-block:: python

    import numpy as np
    from sklearn.decomposition import PCA

    # Create embeddings
    client = EmbeddingClient()
    texts = [
        "This is the first document",
        "This is the second document",
        "And this is the third one",
        "Is this the first document?",
    ]
    embeddings = client.batch_create_embeddings(texts, model_name="text-embedding-ada-002")

    # Convert to numpy array
    embeddings_array = np.array(embeddings)

    # Reduce dimensions with PCA
    pca = PCA(n_components=50)  # Reduce to 50 dimensions
    reduced_embeddings = pca.fit_transform(embeddings_array)

    print(f"Original shape: {embeddings_array.shape}")
    print(f"Reduced shape: {reduced_embeddings.shape}")

Similarity Search
---------------

You can use embeddings for similarity search:

.. code-block:: python

    import numpy as np

    # Create embeddings for a corpus of documents
    client = EmbeddingClient()
    documents = [
        "The quick brown fox jumps over the lazy dog",
        "The five boxing wizards jump quickly",
        "How vexingly quick daft zebras jump",
        "Pack my box with five dozen liquor jugs",
        "The early bird catches the worm",
    ]
    document_embeddings = client.batch_create_embeddings(
        documents, model_name="text-embedding-ada-002"
    )

    # Create an embedding for a query
    query = "jumping animals"
    query_embedding = client.create_embedding(query, model_name="text-embedding-ada-002")

    # Calculate cosine similarity between the query and each document
    similarities = []
    for i, doc_embedding in enumerate(document_embeddings):
        similarity = np.dot(query_embedding, doc_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
        )
        similarities.append((i, similarity))

    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Print results
    print(f"Query: {query}")
    print("Results:")
    for i, similarity in similarities:
        print(f"{similarity:.4f} - {documents[i]}")

Parallel Processing
-----------------

You can use parallel processing to speed up batch embedding creation:

.. code-block:: python

    import concurrent.futures
    import numpy as np

    def create_embeddings_parallel(client, texts, model_name, max_workers=4, batch_size=10):
        """Create embeddings in parallel."""
        # Split texts into batches
        batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]
        
        # Create embeddings for each batch in parallel
        embeddings = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_batch = {
                executor.submit(client.batch_create_embeddings, batch, model_name): i
                for i, batch in enumerate(batches)
            }
            
            for future in concurrent.futures.as_completed(future_to_batch):
                batch_idx = future_to_batch[future]
                try:
                    batch_embeddings = future.result()
                    embeddings.extend(batch_embeddings)
                except Exception as e:
                    print(f"Error processing batch {batch_idx}: {e}")
        
        return embeddings

    # Example usage
    client = EmbeddingClient()
    texts = ["Text " + str(i) for i in range(100)]  # 100 texts
    
    embeddings = create_embeddings_parallel(
        client, texts, "text-embedding-ada-002", max_workers=4, batch_size=10
    )
    
    print(f"Created {len(embeddings)} embeddings")