import json
import boto3
import os

config_path = "/Users/toheed/Projects/Database Backup Utility/src/config.json" 
with open(config_path, 'r') as file:
    config = json.load(file)

def store_on_s3(file_path: str, bucket_name: str, logger):
    try:

        aws_access_key = config['aws']['access_key']
        aws_secret_key = config['aws']['secret_key']
        aws_region = config['aws']['region']


        session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        s3 = session.client('s3')


        logger.info("Uploading backup to S3...")
        s3.upload_file(file_path, bucket_name, os.path.basename(file_path))
        logger.info(f"Backup uploaded to S3 bucket '{bucket_name}' as {os.path.basename(file_path)}")
    except Exception as e:
        raise RuntimeError(f"Error uploading backup to S3: {e}")
