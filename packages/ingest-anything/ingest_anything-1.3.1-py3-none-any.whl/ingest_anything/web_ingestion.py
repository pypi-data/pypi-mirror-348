import os
from typing import Literal, List, Optional
try:
    from .ingestion import (
        BasePydanticVectorStore,
        BaseReader,
        PyMuPDFReader,
        SimpleDirectoryReader,
        uuid,
        StorageContext,
        VectorStoreIndex,
        TextNode,
    )
    from .embeddings import ChonkieAutoEmbedding
    from .add_types import Converter, Chunking, IngestionInput
    from .crawlee_utils import crawler
except ImportError:
    from ingestion import (
        BasePydanticVectorStore,
        BaseReader,
        PyMuPDFReader,
        SimpleDirectoryReader,
        uuid,
        StorageContext,
        VectorStoreIndex,
        TextNode,
    )
    from embeddings import ChonkieAutoEmbedding
    from add_types import Converter, Chunking, IngestionInput
    from crawlee_utils import crawler

default_reader = PyMuPDFReader()
pdf_converter = Converter()

def remove_tmp_files():
    for root, _, fls in os.walk("tmp/ingest_anything/"):
        for f in fls:
            pt = root + "/" + f
            os.remove(pt)

class IngestWeb:
    """
    IngestWeb is a class for ingesting web content into a vector database pipeline.
    This class provides asynchronous methods to fetch web pages, convert them to PDF, chunk the extracted text, and index the resulting data into a vector store for downstream retrieval or search tasks.
    Attributes:
        vector_store (BasePydanticVectorStore): The vector database to store ingested data.
        reader (BaseReader): Reader instance for extracting text from PDF files.
    """
    def __init__(
        self,
        vector_database: BasePydanticVectorStore,
        reader: Optional[BaseReader] = None,
    ) -> None:
        self.vector_store = vector_database
        if reader is None:
            self.reader = default_reader
        self.reader = reader

    async def _batch_fetch_from_web(self, urls: str | List[str]):
        """
        Asynchronously fetches data from a list of URLs using a Crawlee crawler.

        Args
        ----
            urls (str | List[str]): A URL or a list of URLs to fetch data from.

        Returns
        -------
            List[Any]: A list of fetched results for each successfully processed URL.

        Raises
        ------
            ValueError: If none of the provided URLs could be successfully extracted.
        """
        os.makedirs("tmp/ingest_anything", exist_ok=True)
        if isinstance(urls, str):
            urls = [urls]
        try:
            await crawler.run(urls)
        except Exception as e:
            raise ValueError(f"Unable to fetch the URLs at this time because of error: {e.__str__()}")
    async def ingest(
        self,
        urls: str | List[str],
        embedding_model: str,
        chunker: Literal[
            "token", "sentence", "semantic", "sdpm", "late", "neural", "slumber"
        ],
        tokenizer: Optional[str] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
        min_characters_per_chunk: Optional[int] = None,
        min_sentences: Optional[int] = None,
        slumber_genie: Optional[Literal["openai", "gemini"]] = None,
        slumber_model: Optional[str] = None,
    ):
        """
        Ingests web content from one or more URLs, processes it into text chunks, and indexes it using a vector store.

        Args
        ----
            urls (str | List[str]): A single URL or a list of URLs to ingest content from.
            embedding_model (str): The name of the embedding model to use for vectorization.
            chunker (Literal["token", "sentence", "semantic", "sdpm", "late", "neural", "slumber"]):
                The chunking strategy to use for splitting the text.
            tokenizer (Optional[str], optional): The tokenizer to use for chunking. Defaults to None.
            chunk_size (Optional[int], optional): The size of each chunk. Defaults to None.
            chunk_overlap (Optional[int], optional): The number of overlapping tokens or sentences between chunks. Defaults to None.
            similarity_threshold (Optional[float], optional): The similarity threshold for semantic chunking. Defaults to None.
            min_characters_per_chunk (Optional[int], optional): Minimum number of characters per chunk. Defaults to None.
            min_sentences (Optional[int], optional): Minimum number of sentences per chunk. Defaults to None.
            slumber_genie (Optional[Literal["openai", "gemini"]], optional): The Slumber Genie provider for neural chunking. Defaults to None.
            slumber_model (Optional[str], optional): The model name for Slumber Genie. Defaults to None.

        Raises
        ------
            ValueError: If a single URL is provided and cannot be fetched or extracted.

        Returns
        -------
            VectorStoreIndex: An index of the ingested and chunked web content, ready for vector search.
        """
        await self._batch_fetch_from_web(urls)
        chunking = Chunking(
            chunker=chunker,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            similarity_threshold=similarity_threshold,
            min_characters_per_chunk=min_characters_per_chunk,
            min_sentences=min_sentences,
            slumber_genie=slumber_genie,
            slumber_model=slumber_model,
        )
        ingestion_input = IngestionInput(
            files_or_dir="tmp/ingest_anything",
            chunking=chunking,
            tokenizer=tokenizer,
            embedding_model=embedding_model,
        )
        docs = SimpleDirectoryReader(
            input_files=ingestion_input.files_or_dir,
            file_extractor={".pdf": self.reader},
        ).load_data()
        text = "\n\n---\n\n".join([d.text for d in docs])
        chunks = ingestion_input.chunking.chunk(text)
        nodes = [TextNode(text=c.text, id_=str(uuid.uuid4())) for c in chunks]
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        index = VectorStoreIndex(
            nodes=nodes,
            embed_model=ChonkieAutoEmbedding(model_name=embedding_model),
            show_progress=True,
            storage_context=storage_context,
        )
        remove_tmp_files()
        return index
