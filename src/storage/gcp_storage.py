import json
from google.cloud import storage as gcs
import os

def store_on_gcp(file_path: str, bucket_name: str):
    """
    Upload a file to a Google Cloud Storage bucket.
    """
    # Create a client instance
    client = gcs.Client()


