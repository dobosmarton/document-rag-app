import os
import openai

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SimpleFileNodeParser

from .query_engine import get_or_create_storage_context
from .vector_store import get_vector_store_singleton
from .document_store import get_storage_client


openai.api_key = os.getenv("OPENAI_API_KEY")

# define embedding function
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")


def get_document_index() -> VectorStoreIndex:
    document_fs = get_storage_client()
    vector_store = get_vector_store_singleton()
    storage_context = get_or_create_storage_context(
        vector_store,
        fs=document_fs,
    )

    return VectorStoreIndex.from_vector_store(
        storage_context=storage_context,
        vector_store=vector_store,
        embed_model=embed_model,
    )


def add_document(
    document_location: str,
    bucket_name: str,
    index: VectorStoreIndex | None = None,
) -> None:
    file_system = get_storage_client()
    documents = SimpleDirectoryReader(
        input_dir=bucket_name, fs=file_system, input_files=[document_location]
    ).load_data(fs=file_system)

    parsed_nodes = SimpleFileNodeParser().get_nodes_from_documents(documents=documents)
    index.insert_nodes(nodes=parsed_nodes)


def query(
    query_payload: str,
    index: VectorStoreIndex,
) -> str:
    response = index.as_query_engine().query(query_payload)
    return response.response
