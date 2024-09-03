import os
import chromadb
from chromadb.config import Settings
from dotenv import find_dotenv, load_dotenv
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores.types import VectorStore

load_dotenv(find_dotenv("../.env"))

chroma_host = os.getenv("CHROMA_HOST")
chroma_port = os.getenv("CHROMA_PORT")

singleton_vector_store = None


def get_vector_store_singleton() -> VectorStore:
    global singleton_vector_store
    if singleton_vector_store is not None:
        return singleton_vector_store

    chroma_client = chromadb.HttpClient(
        host=chroma_host,
        port=chroma_port,
        settings=Settings(
            allow_reset=True,
            anonymized_telemetry=False,
        ),
    )

    # create client and a new collection
    chroma_collection = chroma_client.get_or_create_collection("documents")

    singleton_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    return singleton_vector_store
