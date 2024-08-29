import os
from dotenv import load_dotenv, find_dotenv
from fastapi import UploadFile
from minio import Minio
from minio.helpers import ObjectWriteResult
from s3fs import core
from fsspec.asyn import AsyncFileSystem

load_dotenv(find_dotenv("../.env"))

bucket_endpoint_url = os.getenv("MINIO_ENDPOINT_URL")
bucket_endpoint = os.getenv("MINIO_ENDPOINT")
bucket_access_key = os.getenv("MINIO_ACCESS_KEY")
bucket_secret_key = os.getenv("MINIO_SECRET_KEY")
bucket_name = os.getenv("MINIO_BUCKET_NAME")


index_persist_dir = bucket_name + "/document_index"

client = Minio(
    endpoint=bucket_endpoint,
    access_key=bucket_access_key,
    secret_key=bucket_secret_key,
    secure=False,
)


def get_storage_client() -> AsyncFileSystem:
    """
    Returns an instance of AsyncFileSystem for accessing the storage client.

    Returns:
        AsyncFileSystem: An instance of AsyncFileSystem for accessing the storage client.
    """
    s3 = core.S3FileSystem(
        key=bucket_access_key,
        secret=bucket_secret_key,
        endpoint_url=bucket_endpoint_url,
    )
    if not s3.exists(bucket_name):
        s3.mkdir(bucket_name)
    return s3


def upload_file(file: UploadFile, object_name: str) -> ObjectWriteResult:
    assert client.bucket_exists(bucket_name)
    try:
        result = client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file.file,
            length=file.size,
            content_type=file.content_type,
        )
        return result
    except Exception as e:
        return f"Error uploading file: {e}"
