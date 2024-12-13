import os
import shutil

def store_locally(file_path: str, destination: str):
    try:
        os.makedirs(destination, exist_ok=True)
        dest_file_path = os.path.join(destination, os.path.basename(file_path))
        shutil.move(file_path, dest_file_path)
        print(f"Backup stored locally at {dest_file_path}")
    except Exception as e:
        raise RuntimeError(f"Error storing backup locally: {e}")
