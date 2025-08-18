from typing import Any, Dict, List, Optional

import mariadb

from app.utils.logger import get_logger

logger = get_logger(__name__)


class MariaDBService:
    """Context manager for MariaDB database connections."""

    def __init__(self, settings: Dict):
        self.config = {
            "user": settings.get("MARIADB_USER"),
            "password": settings.get("MARIADB_PASSWORD"),
            "host": settings.get("MARIADB_HOST"),
            "port": int(settings.get("MARIADB_PORT")),
            "database": settings.get("MARIADB_DATABASE"),
        }
        self.connection = None

    def __enter__(self):
        """Establishes the database connection when entering the 'with' block."""
        try:
            self.connection = mariadb.connect(**self.config)
            logger.info(
                f"""✅ MariaDB connection established to
                {self.config.get('host')}:{self.config.get('port')}/{self.config.get('database')}"""
            )
            return self
        except mariadb.Error as e:
            logger.error(f"❌ Error connecting to MariaDB: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection when exiting the 'with' block."""
        if self.connection:
            try:
                self.connection.close()
                logger.info("✅ MariaDB connection closed.")
            except mariadb.Error as e:
                logger.error(f"❌ Error closing MariaDB connection: {e}")
        # If an exception occurred within the 'with' block, it will be re-raised.

    def execute_query(
        self, query: str, fetch_limit: int = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a query using the existing MariaDB connection.

        Args:
            query: SQL query to execute
            fetch_limit: Maximum number of rows to fetch (None for all)

        Returns:
            List of dictionaries containing query results, or None if error
        """
        if not self.connection:
            logger.error(
                "❌ Cannot execute query: Not connected. Use within a 'with' block."
            )
            return None

        try:
            with self.connection.cursor(dictionary=True) as cursor:
                logger.info("Executing MariaDB query...")
                cursor.execute(query)

                if fetch_limit:
                    results = cursor.fetchmany(fetch_limit)
                else:
                    results = cursor.fetchall()

                logger.info(f"✅ Fetched {len(results)} rows from MariaDB.")
                return results

        except mariadb.Error as e:
            logger.error(f"Error executing MariaDB query: {e}")
            return None
