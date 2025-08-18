import os
from typing import Any, Dict, List, Optional

import oracledb

from app.utils.logger import get_logger

logger = get_logger(__name__)


class OracleService:
    def __init__(self, settings: Dict):
        self.config = {
            "user": settings.get("ORACLE_USER"),
            "password": settings.get("ORACLE_PASSWORD"),
            "dsn": settings.get("ORACLE_DSN"),
        }
        self.connection = None
        if settings.get("ORACLE_INSTANT_CLIENT_PATH") and os.path.isdir(
            settings.get("ORACLE_INSTANT_CLIENT_PATH")
        ):
            logger.info(
                f"Inicializando Oracle Client de: {settings.get('ORACLE_INSTANT_CLIENT_PATH')}"
            )
            oracledb.init_oracle_client(
                lib_dir=settings.get("ORACLE_INSTANT_CLIENT_PATH")
            )

    def __enter__(self):
        """Establishes the database connection when entering the 'with' block."""
        try:
            self.connection = oracledb.connect(**self.config)
            logger.info(f"✅ Connection established to {self.config.get('dsn')}")
            return self
        except Exception as e:
            logger.error(f"❌ Error connecting to Oracle: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection when exiting the 'with' block."""
        if self.connection:
            try:
                self.connection.close()
                logger.info("✅ Oracle connection closed.")
            except Exception as e:
                logger.error(f"❌ Error closing Oracle connection: {e}")
        # If an exception occurred within the 'with' block, it will be re-raised.

    def execute_query(
        self, query: str, fetch_limit: int = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a query using the existing Oracle connection.

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
            with self.connection.cursor() as cursor:
                logger.info("Executing query...")
                cursor.execute(query)

                columns = [desc[0] for desc in cursor.description]

                if fetch_limit:
                    rows = cursor.fetchmany(fetch_limit)
                else:
                    rows = cursor.fetchall()

                results = []
                for row in rows:
                    row_dict = {}
                    for i, col_val in enumerate(row):
                        col_name = columns[i]
                        if isinstance(col_val, oracledb.LOB):
                            row_dict[col_name] = col_val.read()
                        else:
                            row_dict[col_name] = col_val
                    results.append(row_dict)

                logger.info(f"✅ Fetched {len(results)} rows.")
                return results

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None
