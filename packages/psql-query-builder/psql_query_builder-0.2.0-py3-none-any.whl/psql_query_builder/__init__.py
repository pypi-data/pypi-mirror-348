"""
PSQL Query Builder

A tool for generating PostgreSQL queries from natural language using AI.
"""

__version__ = '0.2.0'

from .query_builder import QueryBuilder
from .db_agent import get_database_summary, run_query, parse_postgres_url
from .prompt import generate_sql_prompt
from .query_generator import generate_sql_with_openai

# Import LangChain integration if langchain_core is available
try:
    from .langchain_integration import generate_sql_query, create_psql_query_builder_tools, PSQLQueryBuilderTool
    __all__ = [
        'QueryBuilder',
        'get_database_summary',
        'run_query',
        'parse_postgres_url',
        'generate_sql_prompt',
        'generate_sql_with_openai',
        'generate_sql_query',
        'create_psql_query_builder_tools',
        'PSQLQueryBuilderTool',
    ]
except ImportError:
    # LangChain is not installed
    __all__ = [
        'QueryBuilder',
        'get_database_summary',
        'run_query',
        'parse_postgres_url',
        'generate_sql_prompt',
        'generate_sql_with_openai',
    ]
