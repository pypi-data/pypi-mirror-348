import logging
import os
import sqlite3
from threading import Lock
from typing import Any, Dict, List, Optional, Union, Type, TypeVar

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from ..ThothDbManager import ThothDbManager

T = TypeVar('T', bound='ThothSqliteManager')

class ThothSqliteManager(ThothDbManager):
    """
    SQLite implementation of ThothDbManager.
    """
    _instances = {}
    _lock = Lock()

    @classmethod
    def get_instance(cls: Type[T], 
                    db_id: str,
                    db_root_path: str,
                    db_mode: str = "dev",
                    language: str = "English",
                    **kwargs) -> T:
        """
        Get or create a singleton instance based on connection parameters.
        
        Args:
            db_id (str): Database identifier.
            db_root_path (str): Path to the database root directory.
            db_mode (str, optional): Database mode (dev, prod, etc.). Defaults to "dev".
            **kwargs: Additional parameters.
            
        Returns:
            ThothSqliteManager: An instance of the SQLite manager.
            
        Raises:
            ValueError: If required parameters are missing.
            TypeError: If parameters have incorrect types.
        """
        required_params = ['db_id', 'db_root_path', 'language']

        # Create a dictionary with all parameters
        all_params = {
            'db_id': db_id,
            'db_root_path': db_root_path,
            'db_mode': db_mode,
            'language': language,
            **kwargs
        }

        # Verify that all required parameters are present and not None
        missing_params = [param for param in required_params if all_params.get(param) is None]
        if missing_params:
            raise ValueError(f"Missing required parameter{'s' if len(missing_params) > 1 else ''}: {', '.join(missing_params)}")

        with cls._lock:
            # Create a unique key based on initialization parameters
            instance_key = (db_id, db_root_path, db_mode)
            
            # If the instance doesn't exist or parameters have changed, create a new instance
            if instance_key not in cls._instances:
                instance = cls(**all_params)
                cls._instances[instance_key] = instance
                
            return cls._instances[instance_key]

    def __init__(self, 
                db_id: str,
                db_root_path: str,
                db_mode: str = "dev",
                language: str = "English",
                **kwargs):
        """
        Initialize the SQLite manager.
        
        Args:
            db_id (str): Database identifier.
            db_root_path (str): Path to the database root directory.
            db_mode (str, optional): Database mode (dev, prod, etc.). Defaults to "dev".
            **kwargs: Additional parameters.
        """
        # Remove db_type from kwargs if it exists to avoid duplicate parameter
        kwargs_copy = kwargs.copy()
        if 'db_type' in kwargs_copy:
            del kwargs_copy['db_type']
        
        # Initialize the parent class
        super().__init__(db_root_path=db_root_path, db_mode=db_mode, db_type="sqlite", language=language, **kwargs_copy)
        
        # Only initialize once
        if not hasattr(self, '_initialized') or not self._initialized:
            self._validate_sqlite_params(db_id, db_root_path)
            
            # Set SQLite specific attributes
            self.db_id = db_id
            
            # Set up directory path
            self._setup_directory_path(db_id)
            
            # Ensure the database directory exists
            os.makedirs(self.db_directory_path, exist_ok=True)
            
            # Set up connection string and engine
            db_file_path = self.db_directory_path / f"{self.db_id}.sqlite"
            connection_string = f"sqlite:///{db_file_path}"
            self.engine = create_engine(connection_string)
            
            # Set additional attributes from kwargs
            for key, value in kwargs.items():
                setattr(self, key, value)
            
            # Log initialization
            logging.debug(
                f"Initialized ThothSqliteManager with db_id={db_id}, "
                f"db_path={db_file_path}, db_mode={db_mode}"
            )
            
            self._initialized = True

    def _validate_sqlite_params(self, db_id: str, db_root_path: str) -> None:
        """
        Validate SQLite specific parameters.
        
        Args:
            db_id (str): Database identifier.
            db_root_path (str): Path to the database root directory.
            
        Raises:
            ValueError: If parameters are invalid.
            TypeError: If parameters have incorrect types.
        """
        # Type validation
        if not isinstance(db_id, str):
            raise TypeError("db_id must be a string")
            
        if not isinstance(db_root_path, str):
            raise TypeError("db_root_path must be a string")
            
        # Value validation
        if not db_id:
            raise ValueError("db_id cannot be empty")

    def __repr__(self):
        """
        String representation of the SQLite manager.
        
        Returns:
            str: String representation.
        """
        return (
            f"ThothSqliteManager(db_id='{self.db_id}', "
            f"db_path='{self.db_directory_path / f'{self.db_id}.sqlite'}', "
            f"db_mode='{self.db_mode}')"
        )

    def execute_sql(
        self,
        sql: str,
        params: Optional[Dict] = None,
        fetch: Union[str, int] = "all",
        timeout: int = 60,
    ) -> Any:
        """
        Execute SQL queries on SQLite.

        Args:
            sql (str): The SQL query to execute.
            params (Optional[Dict], optional): Parameters for the SQL query. Defaults to None.
            fetch (Union[str, int], optional): Specifies how to fetch the results. Defaults to "all".
            timeout (int, optional): Timeout for the query execution. Defaults to 60.

        Returns:
            Any: The result of the SQL query execution.
            
        Raises:
            Exception: If there's an error executing the query.
        """
        db_path = self.db_directory_path / f"{self.db_id}.sqlite"
        connection = None
        try:
            connection = sqlite3.connect(str(db_path), timeout=timeout)
            connection.row_factory = sqlite3.Row
            
            cursor = connection.cursor()
            cursor.execute(sql, params or {})
            
            if fetch == "all":
                result = [dict(row) for row in cursor.fetchall()]
            elif fetch == "one":
                row = cursor.fetchone()
                result = dict(row) if row else None
            elif isinstance(fetch, int) and fetch > 0:
                result = [dict(row) for row in cursor.fetchmany(fetch)]
            else:
                connection.commit()
                result = cursor.rowcount
                
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            logging.error(f"Error executing SQL: {str(e)}")
            raise e
        finally:
            if connection:
                connection.close()

    def get_unique_values(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Retrieves unique text values from SQLite database.
        The function is optimized to extract only meaningful values for LSH (Locality-Sensitive Hashing) analysis.

        Filtering Logic:
        1. Analyzes only text type columns
        2. Excludes columns based on name patterns:
            - Suffixes: "Id"
            - Keywords: "_id", " id", "url", "email", "web", "time", "phone", "date", "address"
        
        Value Selection Criteria:
        A column is included if it meets any of these criteria:
        1. Contains "name" in its name
        2. Has average length < 25 characters
        3. Has fewer than 100 distinct values

        Returns:
            Dict[str, Dict[str, List[str]]]: Hierarchical structure of unique values:
            {
                'table_name': {
                    'column_name': ['value1', 'value2', ...]
                }
            }
        """
        inspector = inspect(self.engine)
        
        # Get all table names
        table_names = inspector.get_table_names()
        
        unique_values: Dict[str, Dict[str, List[str]]] = {}
        
        with self.engine.connect() as connection:
            for table_name in table_names:
                logging.info(f"Processing {table_name}")
                
                # Get all columns
                columns_info = inspector.get_columns(table_name)
                
                # Filter text columns
                text_columns = []
                for col in columns_info:
                    col_type = str(col['type']).lower()
                    if 'char' in col_type or 'text' in col_type or 'varchar' in col_type:
                        text_columns.append(col['name'])
                
                table_values: Dict[str, List[str]] = {}
                
                for column in text_columns:
                    if any(
                            keyword in column.lower()
                            for keyword in [
                                "_id",
                                " id",
                                "url",
                                "email",
                                "web",
                                "time",
                                "phone",
                                "date",
                                "address",
                            ]
                    ) or column.endswith("Id"):
                        continue
                    
                    try:
                        # Get statistics about the column
                        query = text(
                            f"""
                            SELECT 
                                COUNT(DISTINCT "{column}") as count_distinct,
                                AVG(LENGTH("{column}")) as avg_length
                            FROM "{table_name}"
                            WHERE "{column}" IS NOT NULL
                            """
                        )
                        stats = connection.execute(query).fetchone()
                        
                        count_distinct = stats[0]
                        avg_length = stats[1]
                        
                        if count_distinct == 0:
                            continue
                            
                        logging.info(
                            f"Column: {column}, count_distinct: {count_distinct}, average_length: {avg_length}"
                        )
                        
                        if (
                                "name" in column.lower()
                                or avg_length < 25
                                or count_distinct < 100
                        ):
                            logging.info(f"Fetching distinct values for {column}")
                            query = text(
                                f"""
                                SELECT DISTINCT "{column}"
                                FROM "{table_name}"
                                WHERE "{column}" IS NOT NULL
                                """
                            )
                            values = [
                                str(value[0])
                                for value in connection.execute(query).fetchall()
                            ]
                            logging.info(f"Number of different values: {len(values)}")
                            table_values[column] = values
                    except SQLAlchemyError as e:
                        logging.error(f"Error processing column {column}: {str(e)}")
                        continue
                
                if table_values:
                    unique_values[table_name] = table_values
        
        return unique_values