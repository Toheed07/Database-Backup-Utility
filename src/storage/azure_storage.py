import json
from azure.storage.blob import BlobServiceClient # type: ignore
import os

config_path = "/Users/toheed/Projects/Database Backup Utility/src/config.json" 
with open(config_path, 'r') as file:
    config = json.load(file)

def store_on_azure(file_path: str, bucket_name: str, logger):
    try:
        connection_string = config['azure']['connection_string']
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=bucket_name, blob=file_path.split('/')[-1])
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        logger.info(f"Backup uploaded to Azure Blob Storage {bucket_name}")
    except Exception as e:
        raise RuntimeError(f"Error uploading backup to Azure Blob Storage: {e}")