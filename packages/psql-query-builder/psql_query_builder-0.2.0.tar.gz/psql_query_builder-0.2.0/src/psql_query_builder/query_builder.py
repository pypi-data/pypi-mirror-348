"""
QueryBuilder class for PSQL Query Builder.

This module provides the main QueryBuilder class that serves as the primary
interface for the Python API of PSQL Query Builder.
"""

import os
from loguru import logger

from .db_agent import parse_postgres_url, run_query, get_database_summary
from .prompt import generate_sql_prompt
from .query_generator import generate_sql_with_openai
from .schema_cache import get_cached_schema, clear_schema_cache
from .error_handler import validate_sql, handle_sql_error


class QueryBuilder:
    """
    Main class for generating and executing SQL queries from natural language.
    
    This class provides a high-level interface for the PSQL Query Builder,
    allowing users to generate and optionally execute SQL queries from
    natural language descriptions.
    """
    
    def __init__(
        self,
        connection_string=None,
        host=None,
        port=None,
        database=None,
        user=None,
        password=None,
        openai_api_key=None,
        model="gpt-4o-mini",
        temperature=0.1,
        schema_cache_path=None,
        schema_cache_ttl=86400,
    ):
        """
        Initialize a new QueryBuilder instance.
        
        Args:
            connection_string: Full PostgreSQL connection string
                (postgresql://user:password@host:port/database)
            host: Database host (used if connection_string not provided)
            port: Database port (used if connection_string not provided)
            database: Database name (used if connection_string not provided)
            user: Database user (used if connection_string not provided)
            password: Database password (used if connection_string not provided)
            openai_api_key: OpenAI API key
            model: OpenAI model to use (default: gpt-4o-mini)
            temperature: Temperature for OpenAI API (default: 0.1)
            schema_cache_path: Path to store schema cache files
            schema_cache_ttl: Schema cache time-to-live in seconds (default: 86400, i.e., 24 hours)
        """
        # Set connection string
        if connection_string:
            self.connection_string = connection_string
        elif all([host, database, user]):
            # Build connection string from individual parameters
            conn_str = f"postgresql://{user}"
            if password:
                conn_str += f":{password}"
            conn_str += f"@{host}"
            if port:
                conn_str += f":{port}"
            conn_str += f"/{database}"
            self.connection_string = conn_str
        else:
            # Try to get from environment variables
            if os.getenv("PSQL_CONNECTION_STRING"):
                self.connection_string = os.getenv("PSQL_CONNECTION_STRING")
            elif all([os.getenv("PSQL_HOST"), os.getenv("PSQL_DATABASE"), os.getenv("PSQL_USER")]):
                conn_str = f"postgresql://{os.getenv('PSQL_USER')}"
                if os.getenv("PSQL_PASSWORD"):
                    conn_str += f":{os.getenv('PSQL_PASSWORD')}"
                conn_str += f"@{os.getenv('PSQL_HOST')}"
                if os.getenv("PSQL_PORT"):
                    conn_str += f":{os.getenv('PSQL_PORT')}"
                conn_str += f"/{os.getenv('PSQL_DATABASE')}"
                self.connection_string = conn_str
            else:
                raise ValueError(
                    "Database connection information must be provided either as a "
                    "connection string or as individual parameters (host, database, user)"
                )
        
        # Set OpenAI API key
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # Set other parameters
        self.model = model
        self.temperature = temperature
        self.schema_cache_path = schema_cache_path
        self.schema_cache_ttl = schema_cache_ttl
        
        # Load database schema
        self._load_schema()
    
    def _load_schema(self, force_refresh=False):
        """
        Load the database schema with caching support.
        
        Args:
            force_refresh: Whether to force a refresh of the cache
        """
        self.schema = get_cached_schema(
            connection_string=self.connection_string,
            cache_path=self.schema_cache_path,
            ttl=self.schema_cache_ttl,
            force_refresh=force_refresh
        )
    
    def refresh_schema(self):
        """
        Force a refresh of the database schema.
        """
        self._load_schema(force_refresh=True)
    
    def clear_schema_cache(self):
        """
        Clear the schema cache for this connection.
        
        Returns:
            Number of cache files removed
        """
        return clear_schema_cache(
            connection_string=self.connection_string,
            cache_path=self.schema_cache_path
        )
    
    def generate_query(self, natural_language_query, include_examples=True):
        """
        Generate a SQL query from a natural language description.
        
        Args:
            natural_language_query: Natural language description of the query
            include_examples: Whether to include example queries in the prompt
            
        Returns:
            Generated SQL query as a string
        """
        # Generate SQL prompt
        prompt = generate_sql_prompt(
            natural_language_query, 
            self.schema, 
            include_examples=include_examples
        )
        
        # Generate SQL query
        sql_query = generate_sql_with_openai(
            prompt,
            api_key=self.openai_api_key,
            model=self.model,
            temperature=self.temperature
        )
        
        return sql_query
    
    def run_query(self, natural_language_query, execute=True, include_examples=True, validate=True):
        """
        Generate and optionally execute a SQL query from a natural language description.
        
        Args:
            natural_language_query: Natural language description of the query
            execute: Whether to execute the generated query (default: True)
            include_examples: Whether to include example queries in the prompt
            validate: Whether to validate the SQL query before execution
            
        Returns:
            If execute=True, returns the query results
            If execute=False, returns the generated SQL query
        """
        # Generate SQL query
        sql_query = self.generate_query(
            natural_language_query, 
            include_examples=include_examples
        )
        
        if not sql_query:
            logger.error("Failed to generate SQL query")
            return None
        
        # If not executing, just return the query
        if not execute:
            return sql_query
        
        # Validate the SQL query if requested
        if validate:
            is_valid, error_message = validate_sql(self.connection_string, sql_query)
            if not is_valid:
                error_info = handle_sql_error(self.connection_string, sql_query, error_message)
                logger.warning(f"SQL validation error: {error_message}")
                # Return the error info along with the query
                return {
                    "query": sql_query,
                    "error": error_info,
                    "results": None
                }
        
        # Execute the query
        try:
            results = run_query(self.connection_string, sql_query)
            return results
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            error_info = handle_sql_error(self.connection_string, sql_query, e)
            return {
                "query": sql_query,
                "error": error_info,
                "results": None
            }
