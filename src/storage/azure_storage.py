import json
from azure.storage.blob import BlobServiceClient # type: ignore
import os

def store_on_azure(file_path: str, container_name: str):
    try:
        # Get connection string from environment
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not conn_str:
            raise ValueError("Missing required AZURE_STORAGE_CONNECTION_STRING environment variable")

        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))

        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

        print(f"Backup uploaded to Azure Blob Storage container '{container_name}' as {os.path.basename(file_path)}")
    except Exception as e:
        raise RuntimeError(f"Error uploading backup to Azure Blob Storage: {e}")