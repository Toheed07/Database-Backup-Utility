import psycopg2
import subprocess
import shutil
from utils.compression import (
    compress_backup,
    compress_backup_tar_file,
    decompress_backup_file,
)
from storage.local_storage import store_locally
from storage.azure_storage import store_on_azure
from storage.s3_storage import store_on_s3
from storage.gcp_storage import store_on_gcp
from utils.notification import send_slack_notification
from utils.encryption import encrypt_file, decrypt_file


class PostgresHandler:
    def __init__(self, host, user, password, database, port=5432):
        self.connection = None
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "dbname": database,
            "port": port,
        }

    def connect(self, logger):
        try:
            self.connection = psycopg2.connect(**self.config)
            logger.info("PostgreSQL connection successful.")
        except psycopg2.Error as e:
            raise ConnectionError(f"PostgreSQL connection failed: {e}")

    def close(self, logger):
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL connection closed.")

    def backup(
        self,
        compress,
        storage,
        notify_slack,
        slack_webhook_url,
        logger,
        encrypt,
        path,
        provider=None,
        bucket=None,
        encrypted_file=None,
    ):
        """
        Backup the PostgreSQL database to a file.

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
            if not shutil.which("pg_dump"):
                raise FileNotFoundError(
                    "pg_dump command not found. Ensure it is installed and in your PATH."
                )

            # Generate pg_dump command
            command = [
                "pg_dump",
                "-h",
                self.config["host"],
                "-p",
                str(self.config["port"]),
                "-U",
                self.config["user"],
                "-d",
                self.config["dbname"],
                "-f",
                path,
                "-b",
                "-v",
                "--large-objects",
                "-F",
                "c",
            ]

            # Execute pg_dump
            with open(path, "w") as backup_file:
                subprocess.run(command, stdout=backup_file, check=True)
            # print(f"Backup successful. File saved to {path}")

            # Handle compression if enabled
            backup_file = path
            if compress:
                backup_file = compress_backup_tar_file(path, f"{path}.gz")

            # Encrypt the backup file
            if encrypt:
                encrypted_file = encrypt_file(backup_file)
            logger.info(f"Encrypted file saved to {encrypted_file}")

            # Handle storage
            self._handle_storage(encrypted_file, storage, provider, bucket, logger)

            # Notify Slack
            if notify_slack and slack_webhook_url:
                send_slack_notification(slack_webhook_url, f"Backup successful: {path}")
            return encrypted_file

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
            decompressed_file = decompress_backup_file(backup_file)

            # Ensure pg_restore is available
            if not shutil.which("pg_restore"):
                raise FileNotFoundError(
                    "pg_restore command not found. Ensure it is installed and in your PATH."
                )

            # Determine the appropriate command based on file extension
            if decompressed_file.endswith(".sql"):
                # Restore plain SQL file using psql
                command = [
                    "psql",
                    "-h",
                    self.config["host"],
                    "-p",
                    str(self.config["port"]),
                    "-U",
                    self.config["user"],
                    "-d",
                    self.config["dbname"],
                    "-f",
                    decompressed_file,
                ]
            elif decompressed_file.endswith(".dump") or decompressed_file.endswith(
                ".backup"
            ):
                # Restore custom format file using pg_restore
                command = [
                    "pg_restore",
                    "-h",
                    self.config["host"],
                    "-p",
                    str(self.config["port"]),
                    "-U",
                    self.config["user"],
                    "-d",
                    self.config["dbname"],
                    "-v",
                    decompressed_file,
                ]
            else:
                raise ValueError(
                    "Unsupported backup file format. Use .sql, .dump, or .backup files."
                )

            # Run the restore command
            subprocess.run(command, check=True)
            logger.info("Restore successful.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed with error code {e.returncode}.")
            raise RuntimeError(f"Restore failed: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise RuntimeError(f"An error occurred during restore: {e}")
