"""
PSQL Query Builder

A tool for generating PostgreSQL queries from natural language using AI.
"""

__version__ = '0.1.0'

from .db_agent import get_database_summary, run_query, parse_postgres_url
from .prompt import generate_sql_prompt
from .query_generator import generate_sql_with_openai

__all__ = [
    'get_database_summary',
    'run_query',
    'parse_postgres_url',
    'generate_sql_prompt',
    'generate_sql_with_openai',
]
