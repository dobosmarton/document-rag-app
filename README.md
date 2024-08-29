# RAG project

A simple project to upload files, build index and ask questions about your documents.

## Tools

- FastAPI
- LlamaIndex
- ChromaDB
- Minio

## Getting started

1. docker-compose up -d
2. poetry install
3. poetry shell
4. uvicorn document_rag:app — reload

## Testing

Use Postman or similar tools to send requests to the backend.

1. Use the `POST http://127.0.0.1:8000/uploadfile` endpoint to upload a file to Minio and build you index in Chroma
2. Use the `POST http://127.0.0.1:8000/conversation` endpoint with a `message` body to ask questions about the document you uploaded
