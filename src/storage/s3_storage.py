import boto3
import os

def store_on_s3(file_path: str, bucket_name: str):
    try:
        print("Uploading backup to S3...")
        print(file_path)
        print(bucket_name)
    #     s3_client = boto3.client("s3")
    #     s3_client.upload_file(file_path, bucket_name, os.path.basename(file_path))
    #     print(f"Backup uploaded to S3 bucket '{bucket_name}' as {os.path.basename(file_path)}")
    except Exception as e:
        raise RuntimeError(f"Error uploading backup to S3: {e}")
