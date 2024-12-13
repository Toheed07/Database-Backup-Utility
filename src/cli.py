import typer
import os
from database.db_factory import get_db_handler
from utils.logging import setup_logger


app = typer.Typer()


logger = setup_logger()


def get_db_params(db_type: str):
    """
    Collects database connection parameters based on the type of database.
    """
    if db_type in ["mysql", "postgres"]:
        return {
            "host": typer.prompt("Enter host"),
            "user": typer.prompt("Enter username"),
            "password": typer.prompt("Enter password", hide_input=True),
            "database": typer.prompt("Enter database name"),
            "port": typer.prompt(
                "Enter port", default=3306 if db_type == "mysql" else 5432
            ),
        }
    elif db_type == "mongo":
        return {
            "host": typer.prompt("Enter host"),
            "port": typer.prompt("Enter port", default=27017),
            "user": typer.prompt("Enter username (leave blank for none)", default=""),
            "password": typer.prompt(
                "Enter password (leave blank for none)", hide_input=True, default=""
            ),
            "database": typer.prompt("Enter database name"),
        }
    elif db_type == "sqlite":
        return {"database": typer.prompt("Enter path to SQLite database")}
    else:
        typer.echo("Unsupported database type!")
        raise typer.Exit()


@app.command()
def backup(
    db_type: str = typer.Option(
        ..., help="Database type (mysql, postgres, mongo, sqlite)"
    ),
    storage: str = typer.Option("local", help="Storage type (local, cloud)"),
    path: str = typer.Option(
        ...,
        help="Local directory path (required for local storage)",
    ),
    provider: str = typer.Option(None, help="Cloud provider (aws, gcp, azure)"),
    bucket: str = typer.Option(
        None, help="Cloud bucket name (required for cloud storage)"
    ),
    notify_slack: bool = typer.Option(False, help="Send Slack notification."),
    slack_webhook_url: str = typer.Option(
        None, help="Slack Webhook URL for notifications."
    ),
    compress: bool = True,
):
    """
    Perform a database backup.
    """
    params = get_db_params(db_type)
    try:
        db_handler = get_db_handler(db_type, **params)
        db_handler.connect(logger=logger)
        typer.echo("Connection successful. Starting backup...")
        compressed_backup_path = db_handler.backup(
            storage=storage,
            path=path,
            provider=provider,
            bucket=bucket,
            notify_slack=notify_slack,
            slack_webhook_url=slack_webhook_url,
            compress=compress,
            logger=logger,
        )
        if compress:
            typer.echo(f"Backup and Compressed saved to: {compressed_backup_path}")
        else:
            typer.echo(f"Backup saved to: {compressed_backup_path}")
        typer.echo("Backup completed successfully.")
    except Exception as e:
        typer.echo(f"Error during backup: {e}")
    finally:
        if "db_handler" in locals():
            db_handler.close(
                logger=logger,
            )


@app.command()
def restore(
    db_type: str = typer.Option(
        ..., help="Database type (mysql, postgres, mongo, sqlite)"
    ),
    backup_path: str = typer.Option(
        ..., help="Path to the backup file (compressed or uncompressed)"
    ),
):
    """
    Restore a database from a backup file.
    """
    if not os.path.exists(backup_path):
        typer.echo(f"Error: Backup file '{backup_path}' does not exist.")
        raise typer.Exit(code=1)

    params = get_db_params(db_type)

    try:
        db_handler = get_db_handler(db_type, **params)
        db_handler.connect(logger=logger)
        typer.echo("Connection successful. Starting restore...")
        # Restore logic per database type
        db_handler.restore(backup_path, logger=logger)
        typer.echo("Restore completed successfully.")
    except Exception as e:
        typer.echo(f"Error during restore: {e}")
    finally:
        if "db_handler" in locals():
            db_handler.close(logger=logger)


@app.command()
def schedule():
    """
    Schedule automatic backups.
    """
    # Placeholder for scheduling logic
    typer.echo("Backup schedule configured successfully.")


@app.command()
def test_connection(
    db_type: str = typer.Option(
        ..., help="Database type (mysql, postgres, mongo, sqlite)"
    )
):
    """
    Test the connection to the database.
    """
    params = get_db_params(db_type)
    try:
        db_handler = get_db_handler(db_type, **params)
        db_handler.connect(logger=logger)
        typer.echo("Database connection test successful!")
    except Exception as e:
        typer.echo(f"Connection test failed: {e}")
    finally:
        if "db_handler" in locals():
            db_handler.close(logger=logger)


if __name__ == "__main__":
    app()


"""
Demo commands:

python cli.py backup --db-type postgres --storage cloud --provider aws --bucket billu --notify-slack  --slack-webhook-url "https://hooks.slack.com/services/TOKEN"
python cli.py backup --db-type mongo --path "/Users/toheed/Projects/Database Backup Utility/src/backups/mongo/" --storage cloud --provider aws --bucket billu --notify-slack  --slack-webhook-url "https://hooks.slack.com/services/TOKEN"
python cli.py restore --db-type mongo --backup-path "/Users/toheed/Projects/Database Backup Utility/src/backups/mongo/blogDB.tar.gz"

"""