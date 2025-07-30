from web_ingestion import IngestWeb, VectorStoreIndex
import pytest
import os
import sys
from dotenv import load_dotenv
import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore

load_dotenv()

# Weaviate config
cluster_url = os.getenv("weaviate_cluster_url")
api_key = os.getenv("weaviate_admin_key")
client_weaviate = weaviate.connect_to_weaviate_cloud(
    cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key),
)
vector_store_weaviate = WeaviateVectorStore(
    weaviate_client=client_weaviate, index_name="TestWeb"
)


@pytest.mark.order1
def test_initialization():
    try:
        ingestor = IngestWeb(vector_database=vector_store_weaviate)
    except Exception:
        ingestor = None
    assert isinstance(ingestor, IngestWeb)

@pytest.mark.asyncio
@pytest.mark.order2
async def test_web_ingestion():
    ingestor = IngestWeb(vector_database=vector_store_weaviate)
    test_cases = [
        {
            "chunker": "sentence",
            "chunk_size": None,
            "chunk_overlap": None,
            "similarity_threshold": None,
            "min_characters_per_chunk": None,
            "min_sentences": None,
            "urls": [
                "https://astrabert.github.io/hophop-science/AI-is-turning-nuclear-a-review/",
                "https://astrabert.github.io/hophop-science/BrAIn-next-generation-neurons/",
                "https://astrabert.github.io/hophop-science/Attention-and-open-source-is-all-you-need/",
            ],
            "tokenizer": "gpt2",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "slumber_genie": None,
            "slumber_model": None,
            "expected": [True, True],
        },
        {
            "chunker": "sentence",
            "chunk_size": None,
            "chunk_overlap": None,
            "similarity_threshold": None,
            "min_characters_per_chunk": None,
            "min_sentences": None,
            "urls": "https://astrabert.github.io/hophop-science/Why-we-dont-need-export-control/",
            "tokenizer": "gpt2",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "slumber_genie": None,
            "slumber_model": None,
            "expected": [True, True],
        },
        {
            "chunker": "sentence",
            "chunk_size": None,
            "chunk_overlap": None,
            "similarity_threshold": None,
            "min_characters_per_chunk": None,
            "min_sentences": None,
            "urls": "https://astrat.github.io/hophop-science/AI-is-turning-nuclear-a-rew/",
            "tokenizer": "gpt2",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "slumber_genie": None,
            "slumber_model": None,
            "expected": None,
        },
    ]
    for test_case in test_cases:
        try:
            result = await ingestor.ingest(
                urls=test_case["urls"],
                embedding_model=test_case["embedding_model"],
                chunker=test_case["chunker"],
                chunk_size=test_case["chunk_size"],
                chunk_overlap=test_case["chunk_overlap"],
                similarity_threshold=test_case["similarity_threshold"],
                min_characters_per_chunk=test_case["min_characters_per_chunk"],
                min_sentences=test_case["min_sentences"],
                tokenizer=test_case["tokenizer"],
                slumber_genie=test_case["slumber_genie"],
                slumber_model=test_case["slumber_model"],
            )
            assert [
                isinstance(result, VectorStoreIndex),
                client_weaviate.collections.exists("TestWeb"),
            ] == test_case["expected"]
        except Exception as e:
            print("ERROR: ", e, file=sys.stderr)
            assert test_case["expected"] is None
