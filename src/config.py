import os
import tarfile

def compress_backup_tar(backup_file, output_file):
    """
    Compress a backup file using tar and gzip.
    
    Args:
        backup_file (str): Path to the folder or file to compress
        output_file (str): Path where the compressed .tar.gz file will be saved
    """
    with tarfile.open(output_file, "w:gz") as tar:
        # Use the full path of the backup file, preserving directory structure
        tar.add(backup_file, arcname=os.path.basename(os.path.normpath(backup_file)))
    print(f"Backup compressed successfully. File saved to {output_file}")
    return output_file

def decompress_backup_tar(backup_file):
    """
    Decompress a .gz tar file, preserving the original folder structure.
    
    Args:
        backup_file (str): Path to the .tar.gz file to decompress
    
    Returns:
        str: Path to the decompressed folder
    """
    if not backup_file.endswith(".tar.gz"):
        raise ValueError("File must be a .tar.gz file")
    
    # Determine the extraction path (same directory as the backup file)
    extraction_path = os.path.dirname(backup_file)
    
    with tarfile.open(backup_file, "r:gz") as tar:
        # Extract all contents, preserving directory structure
        tar.extractall(path=extraction_path)
    
    # Get the name of the extracted folder (without .tar.gz extension)
    decompressed_folder = os.path.join(extraction_path, os.path.splitext(os.path.splitext(os.path.basename(backup_file))[0])[0])
    
    print(f"Backup decompressed successfully. Extracted to {decompressed_folder}")
    return decompressed_folder

# Compress a folder
# compressed_file = compress_backup_tar("/Users/toheed/Projects/Database Backup Utility/src/backups/mongo/blogDB", "/Users/toheed/Projects/Database Backup Utility/src/backups/mongo/compress_backup.tar.gz")

# Decompress the folder
# decompressed_folder = decompress_backup_tar("/Users/toheed/Projects/Database Backup Utility/src/backups/mongo/compress_backup.tar.gz")