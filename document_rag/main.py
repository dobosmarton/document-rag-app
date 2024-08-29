from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from openai import BaseModel
from llama_index.core import VectorStoreIndex

from document_rag.document_store import upload_file as upload_file_to_storage
from document_rag.document_index import (
    get_document_index,
    query,
    add_document,
)


class ConversationPayload(BaseModel):
    message: str


app = FastAPI()


def get_document_index_context():
    try:
        yield get_document_index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document index error: {e}")


@app.post("/conversation", response_model=ConversationPayload)
async def conversation(
    payload: ConversationPayload,
    document_index: Annotated[VectorStoreIndex, Depends(get_document_index_context)],
) -> ConversationPayload:
    try:
        response = query(payload.message, document_index)
        return ConversationPayload(message=response)
    except Exception as e:
        print("Error processing the request", e)
        raise HTTPException(status_code=400, detail="Error processing the request")


@app.post("/uploadfile")
async def upload_file(
    file: UploadFile,
    document_index: Annotated[VectorStoreIndex, Depends(get_document_index_context)],
) -> dict:
    uploaded_file = upload_file_to_storage(file, file.filename)
    add_document(
        document_location=f"{uploaded_file.bucket_name}/{uploaded_file.object_name}",
        bucket_name=uploaded_file.bucket_name,
        index=document_index,
    )
    return {"filename": file.filename}
