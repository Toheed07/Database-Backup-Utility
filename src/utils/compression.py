import tarfile
import os
import gzip
import shutil


def compress_backup(backup_file, output_file):
    """
    Compress a backup file using gzip.

    Args:
        backup_file (str): The path to the backup file.
        output_file (str): The path for the compressed output file.
    """
    with open(backup_file, "rb") as f_in:
        with gzip.open(output_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Backup compressed successfully. File saved to {output_file}")
    return output_file


def compress_backup_tar_file(backup_file, output_file):
    """
    Compress a backup file using tar and gzip.
    """
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(backup_file, arcname=os.path.basename(backup_file))
    print(f"Backup compressed successfully. File saved to {output_file}")
    return output_file


def compress_backup_tar_folder(backup_file, output_file):
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


def decompress_backup_file(backup_file):
    """
    Decompress a compressed backup file.

    :param backup_file: The path to the compressed backup file
    :return: The path to the decompressed SQL file
    """
    if backup_file.endswith(".tar.gz"):
        decompressed_file = backup_file[:-7]  # Remove .tar.gz
        with tarfile.open(backup_file, "r:gz") as tar:
            tar.extractall(path=os.path.dirname(backup_file))
        return decompressed_file

    elif backup_file.endswith(".gz"):
        decompressed_file = backup_file[:-3]  # Remove .gz
        with gzip.open(backup_file, "rb") as f_in:
            with open(decompressed_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        return decompressed_file

    else:
        return backup_file  # Not compressed, return the original file


def decompress_backup_tar_folder(backup_file):
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
    decompressed_folder = os.path.join(
        extraction_path,
        os.path.splitext(os.path.splitext(os.path.basename(backup_file))[0])[0],
    )

    print(f"Backup decompressed successfully. Extracted to {decompressed_folder}")
    return decompressed_folder
