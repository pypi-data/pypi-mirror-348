"""
LangChain integration for PSQL Query Builder.

This module provides tools for integrating PSQL Query Builder with LangChain.
"""

from typing import List, Any, Annotated
from langchain_core.tools import tool, BaseTool, ToolException
from langchain_core.pydantic_v1 import Field

from .query_builder import QueryBuilder


class PSQLQueryBuilderTool(BaseTool):
    """Tool for generating and executing PostgreSQL queries using natural language."""
    
    name: str = "psql_query_builder"
    description: str = "Generate and execute PostgreSQL queries from natural language descriptions"
    
    query_builder: QueryBuilder = Field(exclude=True)
    execute_query: bool = True
    
    def _run(self, query: str) -> Any:
        """Use the tool."""
        try:
            if self.execute_query:
                return self.query_builder.run_query(query)
            else:
                return self.query_builder.generate_query(query)
        except Exception as e:
            raise ToolException(f"Error using PSQL Query Builder: {str(e)}")
    
    async def _arun(self, query: str) -> Any:
        """Use the tool asynchronously."""
        # Since the underlying implementation is synchronous, we just call _run
        return self._run(query)


@tool
def generate_sql_query(
    query: str,
    connection_string: Annotated[str, "PostgreSQL connection string"] = None,
    execute: Annotated[bool, "Whether to execute the query or just return SQL"] = False
) -> str:
    """
    Generate a PostgreSQL query from natural language.
    
    Args:
        query: Natural language description of the query to generate
        connection_string: PostgreSQL connection string (postgresql://user:password@host:port/dbname)
        execute: Whether to execute the query and return results (default: False)
    
    Returns:
        If execute=False: Generated SQL query
        If execute=True: Query results as a string
    """
    try:
        builder = QueryBuilder(connection_string=connection_string)
        
        if execute:
            results = builder.run_query(query)
            if isinstance(results, list):
                # Format results as a string table
                if not results:
                    return "Query executed successfully, but returned no results."
                
                # Simple string formatting of results
                result_str = []
                for row in results:
                    result_str.append(str(row))
                return "\n".join(result_str)
            elif isinstance(results, dict) and results.get("error"):
                return f"Error executing query: {results['error'].get('message', 'Unknown error')}"
            else:
                return f"Query results: {results}"
        else:
            sql = builder.generate_query(query)
            return f"Generated SQL query:\n{sql}"
    except Exception as e:
        return f"Error: {str(e)}"


def create_psql_query_builder_tools(
    connection_string: str = None,
    host: str = None,
    port: int = None,
    database: str = None,
    user: str = None,
    password: str = None,
    openai_api_key: str = None,
) -> List[BaseTool]:
    """
    Create a set of PSQL Query Builder tools for LangChain.
    
    Args:
        connection_string: PostgreSQL connection string
        host: Database host (used if connection_string not provided)
        port: Database port (used if connection_string not provided)
        database: Database name (used if connection_string not provided)
        user: Database user (used if connection_string not provided)
        password: Database password (used if connection_string not provided)
        openai_api_key: OpenAI API key
    
    Returns:
        List of LangChain tools
    """
    # Create a QueryBuilder instance
    query_builder = QueryBuilder(
        connection_string=connection_string,
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        openai_api_key=openai_api_key,
    )
    
    # Create tools
    tools = [
        PSQLQueryBuilderTool(
            name="generate_sql",
            description="Generate a SQL query from natural language without executing it",
            query_builder=query_builder,
            execute_query=False,
        ),
        PSQLQueryBuilderTool(
            name="execute_sql",
            description="Generate and execute a SQL query from natural language",
            query_builder=query_builder,
            execute_query=True,
        ),
    ]
    
    return tools
