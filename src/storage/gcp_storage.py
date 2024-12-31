import json
from google.cloud import storage as gcs
import os
import json

config_path = "/Users/toheed/Projects/Database Backup Utility/src/config.json" 
with open(config_path, 'r') as file:
    config = json.load(file)

def store_on_gcp(file_path: str, bucket_name: str, logger):
    """
    Upload a file to a Google Cloud Storage bucket.
    """
    try:
        service_account_key = config['gcs']['service_account_key']
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
        client = gcs.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(file_path.split('/')[-1])
        blob.upload_from_filename(file_path)
        logger.info(f"Backup uploaded to Google Cloud bucket {bucket_name}")
    except Exception as e:
        raise RuntimeError(f"Error uploading backup to Google Cloud Storage: {e}")
    


