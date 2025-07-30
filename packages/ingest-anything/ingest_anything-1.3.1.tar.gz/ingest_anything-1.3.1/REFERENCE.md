# ingest_anything package

## Submodules

### ingest_anything.add_types module

This module defines the data models for configuring text chunking and ingestion inputs.

- **Classes**

  - `Chunking(BaseModel)`: A Pydantic model for configuring text chunking parameters.

    - Inherits from: `pydantic.BaseModel`
    - Description: This class defines the configuration for different text chunking strategies and their associated parameters.
    - Attributes:
      - `chunker` (`Literal["token", "sentence", "semantic", "sdpm", "late", "slumber", "neural"]`): The chunking strategy to use.
        - `"token"`: Split by number of tokens
        - `"sentence"`: Split by sentences
        - `"semantic"`: Split by semantic similarity
        - `"sdpm"`: Split using sentence distance probability matrix
        - `"late"`: Delayed chunking strategy
        - `"slumber"`: LLM-based chunking using Gemini
        - `"neural"`: Finetuned-for-chunking BERT-based chunking
      - `chunk_size` (`Optional[int]`): The target size for each chunk. Defaults to 512 if not specified.
      - `chunk_overlap` (`Optional[int]`): The number of overlapping units between consecutive chunks. Defaults to 128 if not specified.
      - `similarity_threshold` (`Optional[float]`): The minimum similarity threshold for semantic and SDPM chunking. Defaults to 0.7 if not specified.
      - `min_characters_per_chunk` (`Optional[int]`): The minimum number of characters required for a valid chunk. Defaults to 24 if not specified.
      - `min_sentences` (`Optional[int]`): The minimum number of sentences required for a valid chunk. Defaults to 1 if not specified.
      - `slumber_genie` (`Optional[Literal["openai", "gemini"]]`): The LLM provider for the SlumberChunker. Defaults to "openai".
      - `slumber_model` (`Optional[str]`): The Gemini model name to use for "slumber" chunking. Defaults to "gemini-2.0-flash" or "gpt-4.1" (based on the "slumber_genie" choice) if not specified and "slumber" is chosen.
    - Example:

      ```python
      >>> from ingest_anything.add_types import Chunking
      >>> chunking_config = Chunking(chunker="semantic", chunk_size=256, chunk_overlap=64, similarity_threshold=0.8, min_characters_per_chunk=50, min_sentences=2)
      ```

  - `CodeFiles(BaseModel)`: A Pydantic model for validating and processing lists of code file paths.

    - Inherits from: `pydantic.BaseModel`
    - Description: This class extends BaseModel to handle file path validation, ensuring that all provided paths exist in the filesystem.
    - Attributes:
      - `files` (`List[str]`): A list of file paths to be validated.
    - Raises:
      - `ValueError`: When none of the provided file paths exist in the filesystem.
    - Example:

      ```python
      >>> from ingest_anything.add_types import CodeFiles
      >>> code_files = CodeFiles(files=["file1.py", "file2.py"])
      ```

  - `CodeChunking(BaseModel)`: A Pydantic model for configuring code chunking parameters.

  - Inherits from: `pydantic.BaseModel`
  - Description: This class handles the configuration and validation of parameters used for chunking code into smaller segments, with support for different programming languages and tokenization methods.
  - Attributes:
  - `language`: The programming language of the code to be chunked.
  - `return_type`: The format of the chunked output. Defaults to `"chunks"` if not specified.
  - `tokenizer`: The name of the tokenizer to use. Defaults to `"gpt2"`.
  - `chunk_size`: The maximum size of each chunk in tokens. Defaults to `512`.
  - `include_nodes`: Whether to include AST nodes in the output. Defaults to `False`.
  - Example:

    ```python
    >>> from ingest_anything.add_types import CodeChunking
    >>> code_chunking_config = CodeChunking(language="python", return_type="chunks", tokenizer="gpt2", chunk_size=256, include_nodes=True)
    ```

  - `IngestionInput(BaseModel)`: A class that validates and processes ingestion inputs for document processing.

  - Inherits from: `pydantic.BaseModel`
  - Description: This class handles different types of document inputs and chunking strategies, converting files and setting up appropriate chunking mechanisms based on the specified configuration.
  - Attributes:
  - `files_or_dir`: Path to directory containing files or list of file paths to process.
  - `chunking`: Configuration for the chunking strategy to be used.
  - `tokenizer`
  - `embedding_model`: Name or path of the embedding model to be used.
  - Example:

    ```python
    >>> from ingest_anything.add_types import IngestionInput, Chunking
    >>> ingestion_config = IngestionInput(
    ...     files_or_dir="path/to/documents",
    ...     chunking=Chunking(chunker="token", chunk_size=256, chunk_overlap=64),
    ...     tokenizer="bert-base-uncased",
    ...     embedding_model="sentence-transformers/all-mpnet-base-v2"
    ... )
    ```

### ingest_anything.ingestion module

This module defines the `IngestAnything` and `IngestCode` classes, which handle the ingestion and storage of documents and code files in a vector database.

- **Classes**

  - `IngestAnything`: Provides a high-level interface for ingesting documents, chunking them using various strategies, and indexing them into a vector store for semantic search.

    - `__init__(vector_store: BasePydanticVectorStore, reader: Optional[BaseReader] = None)`

      - Parameters:
        - `vector_store`: The vector store instance where document embeddings will be stored.
        - `reader`: Optional custom document reader. If not provided, a default DoclingReader is used.
      - Example:

        ```python
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> from ingest_anything.ingestion import IngestAnything
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
        >>> ingestor = IngestAnything(vector_store=vector_store)
        ```

    - `ingest(files_or_dir: str | List[str], embedding_model: str, chunker: Literal["token", "sentence", "semantic", "sdpm", "late", "neural", "slumber"], tokenizer: Optional[str] = None, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None, similarity_threshold: Optional[float] = None, min_characters_per_chunk: Optional[int] = None, min_sentences: Optional[int] = None, slumber_genie: Optional[Literal["openai", "gemini"]] = None, slumber_model: Optional[str] = None) -> VectorStoreIndex`

      - Description: Ingest documents from files or directories using the specified chunking strategy and create a searchable vector index.
      - Parameters:
        - `files_or_dir`: Path to file(s) or directory to ingest.
        - `embedding_model`: Name of the embedding model to use: supports OpenAI, HuggingFace, Cohere, Jina AI and Model2Vec
        - `chunker`: Chunking strategy to use.
        - `tokenizer`: Tokenizer to use for chunking.
        - `chunk_size`: Size of chunks.
        - `chunk_overlap`: Number of overlapping tokens/sentences between chunks.
        - `similarity_threshold`: Similarity threshold for semantic chunking.
        - `min_characters_per_chunk`: Minimum number of characters per chunk.
        - `min_sentences`: Minimum number of sentences per chunk.
        - `slumber_genie`: The LLM provider for the SlumberChunker.
        - `slumber_model`: Name of Gemini model to use for chunking, if applicable.
      - Returns:
        - `VectorStoreIndex`: Index containing the ingested and embedded document chunks.
      - Example:

        ```python
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> from ingest_anything.ingestion import IngestAnything
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
        >>> ingestor = IngestAnything(vector_store=vector_store)
        >>> index = ingestor.ingest(
        ...     files_or_dir="path/to/documents",
        ...     embedding_model="sentence-transformers/all-mpnet-base-v2",
        ...     chunker="semantic",
        ...     similarity_threshold=0.8
        ... )
        ```

  - `IngestCode`: is a class for ingesting code files, chunking them, embedding the chunks, and storing them in a vector store for efficient search and retrieval.

    - `__init__(vector_store: BasePydanticVectorStore)`

      - Parameters:
        - `vector_store`: The vector store instance where embedded code chunks will be stored.
      - Example:
        ```python
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> from ingest_anything.ingestion import IngestCode
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_code_collection")
        >>> ingestor = IngestCode(vector_store=vector_store)
        ```

    - `ingest(files: List[str], embedding_model: str, language: str, return_type: Optional[Literal["chunks", "texts"]] = None, tokenizer: Optional[str] = None, chunk_size: Optional[int] = None, include_nodes: Optional[bool] = None)`
      - Description: Ingest code files and create a searchable vector index.
      - Parameters:
        - `files`: List of file paths to ingest
        - `embedding_model`: Name of the HuggingFace embedding model to use
        - `language`: Programming language of the code files
        - `return_type`: Type of return value from chunking
        - `tokenizer`: Name of tokenizer to use
        - `chunk_size`: Size of chunks for text splitting
        - `include_nodes`: Whether to include AST nodes in chunking
      - Returns:
        - `VectorStoreIndex`: Index containing the ingested and embedded code chunks
      - Example:
        ```python
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> from ingest_anything.ingestion import IngestCode
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_code_collection")
        >>> ingestor = IngestCode(vector_store=vector_store)
        >>> index = ingestor.ingest(
        ...     files=["file1.py", "file2.py"],
        ...     embedding_model="sentence-transformers/all-mpnet-base-v2",
        ...     language="python",
        ...     chunk_size=256
        ... )
        ```

### ingest_anything.agent module

This module defines the `IngestAgent` class, which serves as a factory for creating different types of ingestion agents.

- **Classes**

  - `IngestAgent`: An agent factory class for creating different types of ingestion agents.

    - `__init__(self) -> None`: Initializes the IngestAgent class.

      - Parameters:
        - None
      - Example:
        ```python
        >>> from ingest_anything.agent import IngestAgent
        >>> agent_factory = IngestAgent()
        ```

    - `create_agent(self, vector_database: BasePydanticVectorStore, llm: LLM, reader: Optional[BaseReader] = None, ingestion_type: Literal["anything", "code"] = "anything", agent_type: Literal["function_calling", "react"] = "function_calling", tools: Optional[List[BaseTool | Callable | Awaitable]] = None, query_transform: Optional[Literal["hyde", "multi_step"]] = None) -> (IngestAnythingFunctionAgent | IngestAnythingReActAgent | IngestCodeFunctionAgent | IngestCodeReActAgent)`: Creates an agent based on the specified configuration.
      - Description: This method instantiates and returns an appropriate agent based on the ingestion type and agent type specified.
      - Parameters:
        - `vector_database`: Vector database for storing and retrieving embeddings.
        - `llm`: Language model instance to be used by the agent.
        - `reader`: Document reader for processing input files. Defaults to None.
        - `ingestion_type`: Type of content to be ingested. Defaults to "anything".
        - `agent_type`: Type of agent architecture. Defaults to "function_calling".
        - `tools`: List of tools available to the agent. Defaults to None.
        - `query_transform`: Query transformation method. Defaults to None.
      - Returns:
        - `Union[IngestAnythingFunctionAgent, IngestAnythingReActAgent, IngestCodeFunctionAgent, IngestCodeReActAgent]`: An instantiated agent of the appropriate type based on the specified configuration.
      - Example:
        ```python
        >>> from ingest_anything.agent import IngestAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> agent_factory = IngestAgent()
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
        >>> agent = agent_factory.create_agent(vector_database=vector_store, llm=llm, ingestion_type="anything", agent_type="function_calling")
        ```

### ingest_anything.agent_types module

This module defines the agent types for the ingest-anything package, including function calling and ReAct agents for both general content and code ingestion.

- **Classes**

  - `IngestAnythingFunctionAgent(IngestAnything)`: A specialized agent class for ingesting data into a vector database and providing advanced query capabilities using LLMs and optional query transformations.

    - `__init__(self, vector_database: BasePydanticVectorStore, llm: LLM, reader: Optional[BaseReader] = None, tools: Optional[List[BaseTool | Callable | Awaitable]] = None, query_transform: Optional[Literal["hyde", "multi_step"]] = None) -> None`: Initializes the IngestAnythingFunctionAgent.

      - Parameters:
        - `vector_database`: The vector database to use for storing and querying embeddings.
        - `llm`: The large language model used for query processing and transformations.
        - `reader`: Optional reader for ingesting data. Defaults to None.
        - `tools`: Additional tools to be made available to the agent. Defaults to None.
        - `query_transform`: Optional query transformation strategy. Can be "hyde" for HyDEQueryTransform or "multi_step" for StepDecomposeQueryTransform. Defaults to None.
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestAnythingFunctionAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
        >>> agent = IngestAnythingFunctionAgent(vector_database=vector_store, llm=llm)
        ```

    - `ingest(self, files_or_dir: str | List[str], embedding_model: str, chunker: Literal["token", "sentence", "semantic", "sdpm", "late", "neural", "slumber"], tokenizer: Optional[str] = None, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None, similarity_threshold: Optional[float] = None, min_characters_per_chunk: Optional[int] = None, min_sentences: Optional[int] = None, slumber_genie: Optional[Literal["openai", "gemini"]] = None, slumber_model: Optional[str] = None)`: Ingests files or directories into a vector store index using the specified embedding model and chunking strategy.

      - Parameters:
        - `files_or_dir`: Path to a file, directory, or list of files/directories to ingest.
        - `embedding_model`: Name of the embedding model to use for vectorization.
        - `chunker`: Chunking strategy to use for splitting the text.
        - `tokenizer`: Name of the tokenizer to use.
        - `chunk_size`: Size of each chunk.
        - `chunk_overlap`: Number of overlapping tokens or sentences between chunks.
        - `similarity_threshold`: Minimum similarity threshold for semantic chunking.
        - `min_characters_per_chunk`: Minimum number of characters per chunk.
        - `min_sentences`: Minimum number of sentences per chunk.
        - `slumber_genie`: The Slumber Genie provider for neural chunking.
        - `slumber_model`: Name of the Gemini model to use, if applicable.
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestAnythingFunctionAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
        >>> agent = IngestAnythingFunctionAgent(vector_database=vector_store, llm=llm)
        >>> agent.ingest(files_or_dir="path/to/documents", embedding_model="sentence-transformers/all-mpnet-base-v2", chunker="semantic", similarity_threshold=0.8)
        ```

    - `get_agent(self, name: str = "FunctionAgent", description: str = "A useful AI agent", system_prompt: str = "You are a useful assistant who uses the tools available to you whenever it is needed") -> FunctionAgent`: Creates and returns a FunctionAgent instance with the specified name, description, and system prompt.
      - Parameters:
        - `name`: The name of the agent.
        - `description`: A brief description of the agent.
        - `system_prompt`: The system prompt to guide the agent's behavior.
      - Returns:
        - `FunctionAgent`: An instance of FunctionAgent configured with the specified parameters and tools.
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestAnythingFunctionAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
        >>> agent = IngestAnythingFunctionAgent(vector_database=vector_store, llm=llm)
        >>> agent.ingest(files_or_dir="path/to/documents", embedding_model="sentence-transformers/all-mpnet-base-v2", chunker="semantic", similarity_threshold=0.8)
        >>> function_agent = agent.get_agent()
        ```

  - `IngestCodeFunctionAgent(IngestCode)`: A class that combines code ingestion with function agent capabilities.

    - `__init__(self, vector_database: BasePydanticVectorStore, llm: LLM, tools: Optional[List[BaseTool | Callable | Awaitable]] = None, query_transform: Optional[Literal["hyde", "multi_step"]] = None) -> None`: Initializes the IngestCodeFunctionAgent.

      - Parameters:
        - `vector_database`: The vector database to store and retrieve embeddings.
        - `llm`: The language model to use for queries and transformations.
        - `tools`: Additional tools to be used by the agent.
        - `query_transform`: The type of query transformation to apply. Options are "hyde" or "multi_step".
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestCodeFunctionAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_code_collection")
        >>> agent = IngestCodeFunctionAgent(vector_database=vector_store, llm=llm)
        ```

    - `ingest(self, files: List[str], embedding_model: str, language: str, return_type: Optional[Literal["chunks", "texts"]] = None, tokenizer: Optional[str] = None, chunk_size: Optional[int] = None, include_nodes: Optional[bool] = None)`: Ingest code files into the vector database.

      - Parameters:
        - `files`: List of file paths to ingest.
        - `embedding_model`: Name or path of the embedding model to use.
        - `language`: Programming language of the code files.
        - `return_type`: Type of return value from ingestion.
        - `tokenizer`: Tokenizer to use for text splitting.
        - `chunk_size`: Size of text chunks for splitting.
        - `include_nodes`: Whether to include node information.
      - Returns:
        - `VectorStoreIndex`: The index created from ingested files.
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestCodeFunctionAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_code_collection")
        >>> agent = IngestCodeFunctionAgent(vector_database=vector_store, llm=llm)
        >>> agent.ingest(files=["file1.py", "file2.py"], embedding_model="sentence-transformers/all-mpnet-base-v2", language="python", chunk_size=256)
        ```

    - `get_agent(self, name: str = "FunctionAgent", description: str = "A useful AI agent", system_prompt: str = "You are a useful assistant who uses the tools available to you whenever it is needed") -> FunctionAgent`: Create and return a FunctionAgent with configured tools.
      - Parameters:
        - `name`: Name of the agent.
        - `description`: Description of the agent's purpose.
        - `system_prompt`: System prompt for the agent.
      - Returns:
        - `FunctionAgent`: Configured function agent with query engine and additional tools.
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestCodeFunctionAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_code_collection")
        >>> agent = IngestCodeFunctionAgent(vector_database=vector_store, llm=llm)
        >>> agent.ingest(files=["file1.py", "file2.py"], embedding_model="sentence-transformers/all-mpnet-base-v2", language="python", chunk_size=256)
        >>> function_agent = agent.get_agent()
        ```

  - `IngestAnythingReActAgent(IngestAnythingFunctionAgent)`: A ReAct agent implementation for ingesting and processing data.

    - `get_agent(self, name="ReActAgent", description="A useful AI agent", system_prompt="You are a useful assistant who uses the tools available to you whenever it is needed") -> ReActAgent`: Creates and returns a configured ReAct agent instance.
      - Parameters:
        - `name`: Name of the agent.
        - `description`: Description of the agent.
        - `system_prompt`: System prompt for the agent.
      - Returns:
        - `ReActAgent`: Configured ReAct agent instance with query engine and tools.
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestAnythingReActAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_collection")
        >>> agent = IngestAnythingReActAgent(vector_database=vector_store, llm=llm)
        >>> agent.ingest(files_or_dir="path/to/documents", embedding_model="sentence-transformers/all-mpnet-base-v2", chunker="semantic", similarity_threshold=0.8)
        >>> react_agent = agent.get_agent()
        ```

  - `IngestCodeReActAgent(IngestCodeFunctionAgent)`: A class that inherits from IngestCodeFunctionAgent to create a ReAct agent for code ingestion.

    - `get_agent(self, name="ReActAgent", description="A useful AI agent", system_prompt="You are a useful assistant who uses the tools available to you whenever it is needed") -> ReActAgent`: Creates and returns a configured ReActAgent instance with the specified parameters and available tools.
      - Parameters:
        - `name`: The name of the agent.
        - `description`: Description of the agent's purpose.
        - `system_prompt`: The system prompt for the agent.
      - Returns:
        - `ReActAgent`: A configured ReAct agent instance with query engine and other tools.
      - Example:
        ```python
        >>> from ingest_anything.agent_types import IngestCodeReActAgent
        >>> from llama_index.llms.openai import OpenAI
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> llm = OpenAI(api_key="YOUR_API_KEY")
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_code_collection")
        >>> agent = IngestCodeReActAgent(vector_database=vector_store, llm=llm)
        >>> agent.ingest(files=["file1.py", "file2.py"], embedding_model="sentence-transformers/all-mpnet-base-v2", language="python", chunk_size=256)
        >>> react_agent = agent.get_agent()
        ```

### ingest_anything.web_ingestion module

This module defines the `IngestWeb` class, which handles the ingestion of web content into a vector database.

- **Classes**

  - `IngestWeb`: A class for ingesting web content into a vector database pipeline.

    - `__init__(vector_database: BasePydanticVectorStore, reader: Optional[BaseReader] = None) -> None`: Initializes the IngestWeb class.

      - Parameters:
        - `vector_database` (`BasePydanticVectorStore`): The vector database to store ingested data.
        - `reader` (`Optional[BaseReader]`, optional): Reader instance for extracting text from PDF files. Defaults to `None`, which uses a default `PyMuPDFReader`.
      - Example:
        ```python
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> from ingest_anything.web_ingestion import IngestWeb
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_web_collection")
        >>> ingest_web = IngestWeb(vector_database=vector_store)
        ```

    - `ingest(urls: str | List[str], embedding_model: str, chunker: Literal["token", "sentence", "semantic", "sdpm", "late", "neural", "slumber"], tokenizer: Optional[str] = None, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None, similarity_threshold: Optional[float] = None, min_characters_per_chunk: Optional[int] = None, min_sentences: Optional[int] = None, slumber_genie: Optional[Literal["openai", "gemini"]] = None, slumber_model: Optional[str] = None) -> VectorStoreIndex`: Ingests web content from one or more URLs, processes it into text chunks, and indexes it using a vector store.
      - Parameters:
        - `urls` (`str | List[str]`): A single URL or a list of URLs to ingest content from.
        - `embedding_model` (`str`): The name of the embedding model to use for vectorization.
        - `chunker` (`Literal["token", "sentence", "semantic", "sdpm", "late", "neural", "slumber"]`): The chunking strategy to use for splitting the text.
        - `tokenizer` (`Optional[str]`, optional): The tokenizer to use for chunking. Defaults to None.
        - `chunk_size` (`Optional[int]`, optional): The size of each chunk. Defaults to None.
        - `chunk_overlap` (`Optional[int]`, optional): The number of overlapping tokens or sentences between chunks. Defaults to None.
        - `similarity_threshold` (`Optional[float]`, optional): The similarity threshold for semantic chunking. Defaults to None.
        - `min_characters_per_chunk` (`Optional[int]`, optional): Minimum number of characters per chunk. Defaults to None.
        - `min_sentences` (`Optional[int]`, optional): Minimum number of sentences per chunk. Defaults to None.
        - `slumber_genie` (`Optional[Literal["openai", "gemini"]]`, optional): The Slumber Genie provider for neural chunking. Defaults to None.
        - `slumber_model` (`Optional[str]`, optional): The model name for Slumber Genie. Defaults to None.
      - Returns:
        - `VectorStoreIndex`: An index of the ingested and chunked web content, ready for vector search.
      - Example:
        ```python
        >>> from llama_index.vector_stores.qdrant import QdrantVectorStore
        >>> from ingest_anything.web_ingestion import IngestWeb
        >>> vector_store = QdrantVectorStore(client=client, collection_name="my_web_collection")
        >>> ingest_web = IngestWeb(vector_database=vector_store)
        >>> index = await ingest_web.ingest(
        ...     urls=["https://www.example.com", "https://www.wikipedia.org"],
        ...     embedding_model="sentence-transformers/all-mpnet-base-v2",
        ...     chunker="semantic",
        ...     similarity_threshold=0.8
        ... )
        ```
