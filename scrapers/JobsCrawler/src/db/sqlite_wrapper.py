"""
SQLite database wrapper for JobsCrawler.

This module provides a clean interface for database operations,
implementing separation of concerns (SOC) pattern.
"""
import os
import sqlite3
from pathlib import Path
from typing import Any

from src.utils.logger_helper import get_custom_logger

logger = get_custom_logger(__name__)


class JobsDatabase:
    """
    SQLite database wrapper for managing scraped job data.

    Provides a clean interface for database operations with automatic
    schema management and connection handling.

    Attributes
    ----------
        db_path (str): Path to the SQLite database file.
        conn (sqlite3.Connection | None): Database connection object.

    Methods
    -------
        connect(): Establish database connection and create schema.
        get_cursor(): Get a cursor for executing queries.
        commit(): Commit pending transactions.
        close(): Close the database connection.
        create_tables(): Create required database tables.
    """

    def __init__(self, db_path: str = "data/jobs.db"):
        """
        Initialize the JobsDatabase.

        Args:
            db_path (str): Path to the SQLite database file.
                          Defaults to 'data/jobs.db'.
        """
        self.db_path = db_path
        self.conn: sqlite3.Connection | None = None
        self._ensure_data_directory()

    def _ensure_data_directory(self) -> None:
        """Create the data directory if it doesn't exist."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured data directory exists: {db_dir}")

    def connect(self) -> sqlite3.Connection:
        """
        Establish connection to the SQLite database.

        Creates the database file if it doesn't exist and sets up
        required tables automatically.

        Returns
        -------
            sqlite3.Connection: The database connection object.
        """
        self.conn = sqlite3.connect(self.db_path)

        # Enable foreign keys support
        self.conn.execute("PRAGMA foreign_keys = ON")

        # Create tables if they don't exist
        self.create_tables()

        logger.info(f"Connected to database: {self.db_path}")
        return self.conn

    def get_cursor(self) -> sqlite3.Cursor:
        """
        Get a cursor for executing database queries.

        Returns
        -------
            sqlite3.Cursor: Database cursor object.

        Raises
        ------
            ValueError: If connection is not established.
        """
        if not self.conn:
            raise ValueError("Database connection not established. Call connect() first.")
        return self.conn.cursor()

    def commit(self) -> None:
        """Commit pending transactions to the database."""
        if self.conn:
            self.conn.commit()
            logger.debug("Transaction committed")

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
            self.conn = None

    def create_tables(self) -> None:
        """
        Create required database tables if they don't exist.

        Creates the following tables:
        - main_jobs: Primary table for production scraped jobs
        - test: Table for test/development scraped jobs

        Both tables use UNIQUE constraint on 'link' column for
        automatic deduplication via INSERT OR IGNORE.
        """
        if not self.conn:
            raise ValueError("Database connection not established")

        cursor = self.conn.cursor()

        # Schema for scraped jobs
        job_schema = """
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT UNIQUE NOT NULL,
                description TEXT,
                pubdate TEXT,
                location TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                location_tags TEXT,
                status TEXT DEFAULT 'new',
                notes TEXT
            )
        """

        # Create main jobs table
        cursor.execute(job_schema.format(table_name="main_jobs"))
        logger.debug("Created/verified main_jobs table")

        # Create test table
        cursor.execute(job_schema.format(table_name="test"))
        logger.debug("Created/verified test table")

        # Migrate existing tables to add status and notes columns if they don't exist
        self._migrate_add_status_columns(cursor, "main_jobs")
        self._migrate_add_status_columns(cursor, "test")

        # Create index on link for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_main_jobs_link
            ON main_jobs(link)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_test_link
            ON test(link)
        """)

        # Create index on timestamp for filtering
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_main_jobs_timestamp
            ON main_jobs(timestamp)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_test_timestamp
            ON test(timestamp)
        """)

        self.conn.commit()
        logger.info("Database schema created/verified successfully")

    def _migrate_add_status_columns(self, cursor: sqlite3.Cursor, table_name: str) -> None:
        """
        Add status and notes columns to existing tables if they don't exist.

        Args:
            cursor: Database cursor
            table_name: Name of the table to migrate
        """
        # Check if status column exists
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]

        if "status" not in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN status TEXT DEFAULT 'new'")
            logger.info(f"Added 'status' column to {table_name}")

        if "notes" not in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN notes TEXT")
            logger.info(f"Added 'notes' column to {table_name}")

    def get_job_count(self, test: bool = False) -> int:
        """
        Get the total count of jobs in the database.

        Args:
            test (bool): If True, count test table. Otherwise, count main_jobs.

        Returns
        -------
            int: Number of jobs in the table.
        """
        table = "test" if test else "main_jobs"
        cursor = self.get_cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        result = cursor.fetchone()
        return result[0] if result else 0

    def __enter__(self):
        """Context manager entry - establishes connection."""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        """Context manager exit - closes connection."""
        self.close()
