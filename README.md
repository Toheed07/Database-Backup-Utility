# Database-Backup-Utility

This utility provides a robust and flexible solution for backing up and restoring databases. Currently, it supports **MongoDB** and **PostgreSQL**, with plans to extend functionality in the future.

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
    cd backup-restore-utility
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

## Troubleshooting

### Common Errors
1. **`mongodump` or `mongorestore` not found**:
   - Ensure MongoDB utilities are installed and in your PATH.
   - Example installation for Ubuntu:
     ```bash
     sudo apt install mongodb-clients
     ```

2. **Permission Denied**:
   - Ensure the backup folder has write permissions.
   - Example command to fix permissions:
     ```bash
     chmod -R 755 ./backups
     ```

3. **Unsupported File Format**:
   - Ensure you are using `.tar.gz` files for backups.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

---

## Future Plans
- Add support for more database types (e.g., MySQL, SQLite).
- Implement scheduled backups using a task scheduler.

---

## Authors
- Toheed (toheedjamaal9@gmail.com)

