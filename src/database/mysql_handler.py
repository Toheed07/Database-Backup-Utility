import mysql.connector  # type: ignore
import subprocess
import shutil
import os

class MySQLHandler:
    def __init__(self, host, user, password, database, port=3306):
        self.connection = None
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port,
        }

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("MySQL connection successful.")
        except mysql.connector.Error as e:
            raise ConnectionError(f"MySQL connection failed: {e}")
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("MySQL connection closed.")

    def backup(self, backup_path="backup.sql"):
        """
        Backup the MySQL database to a file.

        Args:
            backup_path (str): The file path to save the backup.
        """
        try:
            # Ensure mysqldump is available
            if not shutil.which("mysqldump"):
                raise FileNotFoundError("mysqldump command not found. Ensure it is installed and in your PATH.")

            command = [
                "mysqldump",
                "-h", self.config["host"],
                "-P", str(self.config["port"]),
                "-u", self.config["user"],
                f"--password={self.config['password']}",
                self.config["database"],
            ]

            with open(backup_path, "w") as backup_file:
                subprocess.run(command, stdout=backup_file, check=True)
            print(f"Backup successful. File saved to {backup_path}")

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Backup failed: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during backup: {e}")
