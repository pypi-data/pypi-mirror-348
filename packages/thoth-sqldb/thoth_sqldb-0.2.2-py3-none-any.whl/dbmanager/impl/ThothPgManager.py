import logging
from threading import Lock
from typing import Any, Dict, List, Optional, Union, Type, TypeVar
import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy import create_engine, TextClause, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from ..ThothDbManager import ThothDbManager

T = TypeVar('T', bound='ThothPgManager')

class ThothPgManager(ThothDbManager):
    """
    PostgreSQL implementation of ThothDbManager.
    """
    _instances = {}
    _lock = Lock()

    @classmethod
    def get_instance(cls: Type[T], 
                    host: str, 
                    port: int, 
                    dbname: str, 
                    user: str, 
                    password: str, 
                    db_root_path: str, 
                    db_mode: str = "dev", 
                    schema: str = "public",
                    language: str = "English",
                    **kwargs) -> T:
        """
        Get or create a singleton instance based on connection parameters.
        
        Args:
            host (str): Database host.
            port (int): Database port.
            dbname (str): Database name.
            user (str): Database user.
            password (str): Database password.
            db_root_path (str): Path to the database root directory.
            db_mode (str, optional): Database mode (dev, prod, etc.). Defaults to "dev".
            schema (str, optional): Database schema. Defaults to "public".
            **kwargs: Additional parameters.
            
        Returns:
            ThothPgManager: An instance of the PostgreSQL manager.
            
        Raises:
            ValueError: If required parameters are missing.
            TypeError: If parameters have incorrect types.
            :param schema:
            :param db_mode:
            :param password:
            :type db_root_path: object
            :param user:
            :param dbname:
            :param port:
            :param host:
            :param language:
        """
        required_params = ['host', 'port', 'dbname', 'user', 'password', 'db_root_path','language']

        # Create a dictionary with all parameters
        all_params = {
            'host': host,
            'port': port,
            'dbname': dbname,
            'user': user,
            'password': password,
            'db_root_path': db_root_path,
            'db_mode': db_mode,
            'schema': schema,
            'language': language,
            **kwargs
        }

        # Verify that all required parameters are present and not None
        missing_params = [param for param in required_params if all_params.get(param) is None]
        if missing_params:
            raise ValueError(f"Missing required parameter{'s' if len(missing_params) > 1 else ''}: {', '.join(missing_params)}")

        with cls._lock:
            # Create a unique key based on initialization parameters
            instance_key = (host, port, dbname, user, password, db_root_path, db_mode,schema)
            
            # If the instance doesn't exist or parameters have changed, create a new instance
            if instance_key not in cls._instances:
                instance = cls(**all_params)
                cls._instances[instance_key] = instance
                
            return cls._instances[instance_key]

    def __init__(self, 
                host: str, 
                port: int, 
                dbname: str, 
                user: str, 
                password: str, 
                db_root_path: str, 
                db_mode: str = "dev", 
                schema: str = "public",
                language: str = "English",
                **kwargs):
        """
        Initialize the PostgreSQL manager.
        
        Args:
            host (str): Database host.
            port (int): Database port.
            dbname (str): Database name.
            user (str): Database user.
            password (str): Database password.
            db_root_path (str): Path to the database root directory.
            db_mode (str, optional): Database mode (dev, prod, etc.). Defaults to "dev".
            schema (str, optional): Database schema. Defaults to "public".
            **kwargs: Additional parameters.
        """
        # Remove db_type from kwargs if it exists to avoid duplicate parameter
        kwargs_copy = kwargs.copy()
        if 'db_type' in kwargs_copy:
            del kwargs_copy['db_type']
        
        # Initialize the parent class
        super().__init__(db_root_path=db_root_path, db_mode=db_mode, db_type="postgresql", language=language, **kwargs_copy)
        
        # Only initialize once
        if not hasattr(self, '_initialized') or not self._initialized:
            self._validate_pg_params(host, port, dbname, user, password)
            
            # Set PostgreSQL specific attributes
            self.host = host
            self.port = port
            self.dbname = dbname
            self.user = user
            self.password = password
            self.schema = schema
            self.language = language
            
            # Set additional attributes from kwargs
            for key, value in kwargs.items():
                setattr(self, key, value)
            
            # Set up connection string and engine
            connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
            self.engine = create_engine(connection_string)
            
            # Set up directory path
            self._setup_directory_path(dbname)
            
            # Log initialization
            logging.debug(
                f"Initialized ThothPgManager with host={host}, port={port}, dbname={dbname}, "
                f"user={user}, schema={schema}"
            )
            
            self._initialized = True

    def _validate_pg_params(self, host: str, port: int, dbname: str, user: str, password: str) -> None:
        """
        Validate PostgreSQL specific parameters.
        
        Args:
            host (str): Database host.
            port (int): Database port.
            dbname (str): Database name.
            user (str): Database user.
            password (str): Database password.
            
        Raises:
            ValueError: If parameters are invalid.
            TypeError: If parameters have incorrect types.
        """
        # Type validation
        if not isinstance(port, int):
            raise TypeError("port must be an integer")
            
        # Value validation
        if not (1 <= port <= 65535):
            raise ValueError("port must be between 1 and 65535")
            
        # Required parameters validation
        if not host or not dbname or not user or password is None:
            raise ValueError("host, dbname, user, and password are required parameters")

    def __repr__(self):
        """
        String representation of the PostgreSQL manager.
        
        Returns:
            str: String representation.
        """
        return (
            f"ThothPgManager(host='{self.host}', port={self.port}, dbname='{self.dbname}', "
            f"user='{self.user}', schema='{self.schema}', db_mode='{self.db_mode}')"
        )

    def execute_sql(
        self,
        sql: str,
        params: Optional[Dict] = None,
        fetch: Union[str, int] = "all",
        timeout: int = 60,
    ) -> Any:
        """
        Execute SQL queries on PostgreSQL.

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
        connection = None
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor,
            )
            
            with connection.cursor() as cursor:
                cursor.execute(sql, params or {})
                
                if fetch == "all":
                    result = cursor.fetchall()
                elif fetch == "one":
                    result = cursor.fetchone()
                elif isinstance(fetch, int) and fetch > 0:
                    result = cursor.fetchmany(fetch)
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
        Retrieves unique text values from PostgreSQL database, excluding primary keys.
        The function is optimized to extract only meaningful values for LSH (Locality-Sensitive Hashing) analysis.

        Filtering Logic:
        1. Excludes primary keys to avoid non-meaningful identifier values
        2. Analyzes only text (str) type columns
        3. Excludes columns based on name patterns:
            - Suffixes: "Id"
            - Keywords: "_id", " id", "url", "email", "web", "time", "phone", "date", "address"
        
        Value Selection Criteria:
        A column is included if it meets any of these criteria:
        1. Contains "name" in its name AND has less than 5MB total data
        2. Has less than 2MB total data AND average length < 25 characters
        3. Has fewer than 100 distinct values

        Optimizations:
        - Pre-calculates statistics (sum length, count distinct) before extracting values
        - Uses distinct queries to avoid duplicates
        - Ignores NULL values
        
        Returns:
            Dict[str, Dict[str, List[str]]]: Hierarchical structure of unique values:
            {
                'table_name': {
                    'column_name': ['value1', 'value2', ...]
                }
            }

        Example:
            {
                'employees': {
                    'department': ['HR', 'IT', 'Sales'],
                    'position': ['Manager', 'Developer', 'Analyst']
                }
            }

        Notes:
            - Primarily used for building LSH indexes
            - Size thresholds (5MB, 2MB) are optimized to balance completeness and performance
            - Detailed logging helps with debugging and monitoring
        """
        inspector = inspect(self.engine)

        # Get all table names
        table_names = inspector.get_table_names(schema=self.schema)

        # Get primary keys
        primary_keys = []
        for table_name in table_names:
            pk_constraint = inspector.get_pk_constraint(table_name, schema=self.schema)
            primary_keys.extend(pk_constraint["constrained_columns"])

        unique_values: Dict[str, Dict[str, List[str]]] = {}

        with self.engine.connect() as connection:
            for table_name in table_names:
                logging.info(f"Processing {table_name}")

                # Get text columns that are not primary keys
                columns = [
                    col["name"]
                    for col in inspector.get_columns(table_name, schema=self.schema)
                    if col["type"].python_type == str
                       and col["name"] not in primary_keys
                ]

                table_values: Dict[str, List[str]] = {}

                for column in columns:
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
                        query = text(
                            f"""
                                SELECT SUM(LENGTH(unique_values)), COUNT(unique_values)
                                FROM (
                                    SELECT DISTINCT {column} AS unique_values
                                    FROM {self.schema}.{table_name}
                                    WHERE {column} IS NOT NULL
                                ) AS subquery
                            """
                        )
                        result = connection.execute(query).fetchone()
                    except SQLAlchemyError:
                        result = (0, 0)

                    sum_of_lengths, count_distinct = result
                    if sum_of_lengths is None or count_distinct == 0:
                        continue

                    average_length = sum_of_lengths / count_distinct
                    logging.info(
                        f"Column: {column}, sum_of_lengths: {sum_of_lengths}, count_distinct: {count_distinct}, average_length: {average_length}"
                    )

                    if (
                            ("name" in column.lower() and sum_of_lengths < 5000000)
                            or (sum_of_lengths < 2000000 and average_length < 25)
                            or count_distinct < 100
                    ):
                        logging.info(f"Fetching distinct values for {column}")
                        try:
                            query = text(
                                f"""
                                    SELECT DISTINCT {column}
                                    FROM {self.schema}.{table_name}
                                    WHERE {column} IS NOT NULL
                                """
                            )
                            values = [
                                str(value[0])
                                for value in connection.execute(query).fetchall()
                            ]
                        except SQLAlchemyError:
                            values = []
                        logging.info(f"Number of different values: {len(values)}")
                        table_values[column] = values

                unique_values[table_name] = table_values

        return unique_values
