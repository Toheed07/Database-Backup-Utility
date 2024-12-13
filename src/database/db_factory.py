import mysql.connector # type: ignore
from database.mysql_handler import MySQLHandler
from database.postgres_handler import PostgresHandler
from database.mongo_handler import MongoDBHandler

class UnsupportedDBTypeError(Exception):
    """Custom exception for unsupported database types."""
    pass

def get_db_handler(db_type, **kwargs):
    """
    Factory function to return the appropriate database handler.

    Args:
        db_type (str): The type of the database (mysql, postgres, mongo, sqlite).
        **kwargs: Additional connection parameters like host, user, password, etc.

    Returns:
        A database handler instance.

    Raises:
        UnsupportedDBTypeError: If an unsupported database type is provided.
    """
    db_type = db_type.lower()
    
    if db_type == "mysql":
        return MySQLHandler(**kwargs)
    elif db_type == "postgres":
        return PostgresHandler(**kwargs)
    elif db_type == "mongo":
        return MongoDBHandler(**kwargs)
    else:
        raise UnsupportedDBTypeError(f"Unsupported database type: {db_type}")
