from pymongo import MongoClient
import subprocess
import shutil
from utils.compression import compress_backup_tar_folder, decompress_backup_tar_folder
from storage.local_storage import store_locally
from storage.azure_storage import store_on_azure
from storage.s3_storage import store_on_s3
from storage.gcp_storage import store_on_gcp
from utils.notification import send_slack_notification
from utils.encryption import encrypt_file, decrypt_file


class MongoDBHandler:
    def __init__(self, host, port, user=None, password=None, database=None):
        """
        MongoDB Handler to manage connections and operations.

        Args:
            host (str): MongoDB host address.
            port (int): MongoDB port.
            user (str): MongoDB username (optional).
            password (str): MongoDB password (optional).
            database (str): Database name to connect to (optional).
        """
        self.client = None
        self.database = database
        self.config = {
            "host": host,
            "port": port,
            "username": user,
            "password": password,
        }

    def connect(self, logger):
        """
        Connect to MongoDB using the provided configuration.

        Args:
            logger: Logger instance for logging.

        Raises:
            ConnectionError: If the connection fails.
        """
        try:
            # Remove None values from the configuration
            clean_config = {k: v for k, v in self.config.items() if v is not None}

            # Establish a connection
            self.client = MongoClient(**clean_config)
            logger.info("MongoDB connection successful.")

            # Check if database exists
            if self.database:
                if self.database not in self.client.list_database_names():
                    logger.warning(
                        f"Database '{self.database}' does not exist. It will be created upon first use."
                    )
            return self.client

        except Exception as e:
            raise ConnectionError(f"MongoDB connection failed: {e}")

    def close(self, logger):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    def backup(
        self,
        compress,
        storage,
        path,
        notify_slack,
        encrypt,
        slack_webhook_url,
        logger,
        provider=None,
        bucket=None,
        encrypted_file=None,
    ):
        """
        Perform a backup of the MongoDB database.

        Args:
            compress (bool): Whether to compress the backup file.
            storage (str): Storage type ('local' or 'cloud').
            path (str): Path to save the backup file.
            provider (str, optional): Cloud provider ('aws', 'gcp', 'azure'). Required for cloud storage.
            bucket (str, optional): Cloud bucket name. Required for cloud storage.
        """
        try:
            logger.info("Starting backup...")
            # Ensure pg_dump is available
            if not shutil.which("mongodump"):
                raise FileNotFoundError(
                    "mongodump command not found. Ensure it is installed and in your PATH."
                )

            # Construct the mongodump command
            command = [
                "mongodump",
                "--host",
                self.config["host"],
                "--db",
                self.database,
                "--port",
                str(self.config["port"]),
                "--out",
                path,
            ]

            subprocess.run(command, check=True)
            logger.info(f"Backup successful. Files saved to {path}")

            # Handle compression if enabled
            backup_file = path

            if compress:
                backup_file = compress_backup_tar_folder(
                    path, f"{path}/{self.database}.tar.gz"
                )

            # Encrypt the backup file
            if encrypt:
                encrypted_file = encrypt_file(backup_file)
            logger.info(f"Encrypted file saved to {encrypted_file}")

            # Handle storage
            self._handle_storage(encrypted_file, storage, provider, bucket, logger)

            # Notify Slack
            if notify_slack and slack_webhook_url:
                send_slack_notification(slack_webhook_url, f"Backup successful: {path}")
            return backup_file

        except subprocess.CalledProcessError as e:

            if notify_slack and slack_webhook_url:
                send_slack_notification(slack_webhook_url, f"Backup failed: {e}")
            logger.error(f"Backup failed: {e}")
            raise RuntimeError(f"Backup failed: {e}")

        except Exception as e:
            logger.error(f"An error occurred during backup: {e}")
            raise RuntimeError(f"An error occurred during backup: {e}")

    def _handle_storage(self, file_path, storage, provider, bucket, logger):
        """
        Handle the storage of the backup file.

        Args:
            file_path (str): The file path to store.
            storage (str): Storage type ('local' or 'cloud').
            provider (str, optional): Cloud provider ('aws', 'gcp', 'azure').
            bucket (str, optional): Cloud bucket name.
        """
        if storage == "cloud":
            if not provider or not bucket:
                raise ValueError(
                    "Cloud provider and bucket name are required for cloud storage."
                )
            self._upload_to_cloud(file_path, provider, bucket, logger)
        elif storage == "local":
            logger.info(f"Backup stored locally at {file_path}")
        else:
            raise ValueError("Unsupported storage type. Choose 'local' or 'cloud'.")

    def _upload_to_cloud(self, file_path, provider, bucket, logger):
        """
        Upload the backup file to the cloud.

        Args:
            file_path (str): Path to the file to upload.
            provider (str): Cloud provider ('aws', 'gcp', 'azure').
            bucket (str): Cloud bucket name.
        """
        try:
            if provider == "aws":
                store_on_s3(file_path, bucket, logger)
            elif provider == "gcp":
                store_on_gcp(file_path, bucket, logger)
            elif provider == "azure":
                store_on_azure(file_path, bucket, logger)
            else:
                raise ValueError("Unsupported cloud provider.")
            logger.info(f"Backup uploaded to {provider} bucket '{bucket}'")

        except Exception as e:
            logger.error(f"Failed to upload backup to cloud: {e}")
            raise RuntimeError(f"Error uploading to cloud: {e}")

    def restore(self, backup_file, logger):
        """
        Restore the PostgreSQL database from a backup file.

        Args:
            backup_file (str): The path to the backup file.
        """
        try:
            logger.info("Starting restore...")

            # Decrypt the backup file
            logger.info("Decrypting the backup file...")
            backup_file = decrypt_file(backup_file)
            logger.info(f"Decrypted file available at {backup_file}")

            # Decompress the backup file
            decompressed_file = decompress_backup_tar_folder(backup_file)
            # Ensure mongorestore is available
            if not shutil.which("mongorestore"):
                raise FileNotFoundError(
                    "mongorestore command not found. Ensure it is installed and in your PATH."
                )

            # Determine the appropriate command based on file extension
            command = [
                "mongorestore",
                "--host",
                self.config["host"],
                "--port",
                str(self.config["port"]),
                "--db",
                self.database,
                "--dir",
                decompressed_file,
            ]

            # Run the restore command
            subprocess.run(command, check=True)
            logger.info("Restore successful.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed with error code {e.returncode}.")
            raise RuntimeError(f"Restore failed: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise RuntimeError(f"An error occurred during restore: {e}")
