# Database-Backup-Utility

This utility provides a robust and flexible solution for backing up and restoring databases. Currently, it supports **MongoDB** and **PostgreSQL**, with plans to extend functionality in the future.

Project Link : https://roadmap.sh/projects/database-backup-utility

## Features
- **Backup**: Automatically compresses and stores backups for MongoDB and PostgreSQL.
- **Restore**: Decompresses and restores data from backup files.
- **Logging**: Provides detailed logs for backup and restore operations, including timestamps, statuses, and errors.

---

## Prerequisites

### General Requirements
- Python 3.7+
- Required Python libraries: `requests`, `pymongo`, `psycopg2-binary`, `tarfile`, `shutil`, `subprocess`
- Ensure that the following utilities are installed on your system and available in your PATH:
  - `mongodump` (for MongoDB backups)
  - `mongorestore` (for MongoDB restores)
  - `pg_dump` (for PostgreSQL backups)
  - `psql` (for PostgreSQL restores)

### MongoDB Requirements
- A running MongoDB instance.
- Authentication credentials (if enabled).

### PostgreSQL Requirements
- A running PostgreSQL server.
- Database user with appropriate privileges for backup and restore operations.

---

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/Toheed07/Database-Backup-Utility.git
    cd Database-Backup-Utility
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For macOS/Linux
    venv\Scripts\activate  # For Windows
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure the required utilities (`mongodump`, `mongorestore`, `pg_dump`, `psql`) are installed and accessible.

---

## Usage
### Command-Line Interface (CLI)
The utility provides a CLI interface for both backup and restore operations.

#### Backup Command
```bash
python cli.py backup --db-type <mongo|postgres> --path <path-to-backup-folder>
```

**Arguments:**
- `--db-type`: The type of database (e.g., `mongo`, `postgres`).
- `--path`: The directory where the backup file will be stored.

**Examples:**
- Backup a MongoDB database:
    ```bash
    python cli.py backup --db-type mongo --path ./backups/mongo
    ```
- Backup a PostgreSQL database:
    ```bash
    python cli.py backup --db-type postgres --path ./backups/postgres
    ```

#### Restore Command
```bash
python cli.py restore --db-type <mongo|postgres> --backup-path <path-to-backup-file>
```

**Arguments:**
- `--db-type`: The type of database (e.g., `mongo`, `postgres`).
- `--backup-path`: The path to the backup file to restore.

**Examples:**
- Restore a MongoDB database:
    ```bash
    python cli.py restore --db-type mongo --backup-path ./backups/mongo/mongo_backup.tar.gz
    ```
- Restore a PostgreSQL database:
    ```bash
    python cli.py restore --db-type postgres --backup-path ./backups/postgres/postgres_backup.tar.gz
    ```

---
## Encryption
The utility supports encryption and decrytion for both backup and restore operations automatically. If you want to disable this operation, you can pass `--encrypt=False`.

## Logging
The utility uses Python’s `logging` module to provide detailed logs. Logs are stored in the `backup_utility` file.

### Example Log Output
```
2024-12-13 08:45:40,318 - INFO - Backup process started.
2024-12-13 08:45:42,510 - INFO - Backup successful. File saved to ./backups/mongo/mongo_backup.tar.gz
2024-12-13 09:00:10,123 - INFO - Restore process started.
2024-12-13 09:02:15,567 - ERROR - Restore failed with error code 1.
```

---


## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

---

## Future Plans
- Add support for more database types (e.g., MySQL, SQLite).
- Implement scheduled backups.

---

## Author
- Toheed (toheedjamaal9@gmail.com)
