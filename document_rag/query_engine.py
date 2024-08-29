from typing import Optional
from llama_index.core.vector_stores.types import VectorStore
from llama_index.core import StorageContext
from fsspec.asyn import AsyncFileSystem

from document_rag.document_store import index_persist_dir


def get_storage_context(
    persist_dir: str,
    vector_store: VectorStore,
    fs: Optional[AsyncFileSystem] = None,
) -> StorageContext:
    return StorageContext.from_defaults(
        persist_dir=persist_dir, vector_store=vector_store, fs=fs
    )


def get_or_create_storage_context(
    vector_store: VectorStore,
    fs: Optional[AsyncFileSystem] = None,
) -> StorageContext:
    try:
        return get_storage_context(
            persist_dir=index_persist_dir,
            vector_store=vector_store,
            fs=fs,
        )
    except ValueError:
        print("Could not find storage context in S3. Creating new storage context.")
        storage_context = StorageContext.from_defaults(vector_store=vector_store, fs=fs)
        storage_context.persist(persist_dir=index_persist_dir, fs=fs)
        return storage_context
