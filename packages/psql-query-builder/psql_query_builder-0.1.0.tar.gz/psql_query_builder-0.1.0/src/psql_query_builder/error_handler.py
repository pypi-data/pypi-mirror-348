"""
Enhanced error handling for PSQL Query Builder.

This module provides improved error handling and feedback for SQL queries,
helping users understand and fix issues with generated queries.
"""

import re
import difflib
from loguru import logger
import psycopg2


def find_similar_columns(connection_string, table_name, column_name, threshold=0.6):
    """
    Find column names similar to the given column name in the specified table.
    
    Args:
        connection_string: PostgreSQL connection string
        table_name: Name of the table to check
        column_name: Column name that caused the error
        threshold: Similarity threshold (0-1)
        
    Returns:
        List of similar column names
    """
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Extract schema and table name
        parts = table_name.split('.')
        if len(parts) == 2:
            schema, table = parts
        else:
            schema = 'public'
            table = table_name
        
        # Get all columns in the table
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
        """, (schema, table))
        
        all_columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        # Find similar columns
        similar_columns = []
        for col in all_columns:
            similarity = difflib.SequenceMatcher(None, column_name.lower(), col.lower()).ratio()
            if similarity >= threshold:
                similar_columns.append((col, similarity))
        
        # Sort by similarity (highest first)
        similar_columns.sort(key=lambda x: x[1], reverse=True)
        
        return [col for col, _ in similar_columns[:5]]  # Return top 5 matches
    
    except Exception as e:
        logger.error(f"Error finding similar columns: {e}")
        return []


def find_similar_tables(connection_string, table_name, threshold=0.6):
    """
    Find table names similar to the given table name.
    
    Args:
        connection_string: PostgreSQL connection string
        table_name: Table name that caused the error
        threshold: Similarity threshold (0-1)
        
    Returns:
        List of similar table names
    """
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Get all tables in the database
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            AND table_type = 'BASE TABLE'
        """)
        
        all_tables = [f"{row[0]}.{row[1]}" if row[0] != 'public' else row[1] 
                     for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        # Find similar tables
        similar_tables = []
        for tbl in all_tables:
            similarity = difflib.SequenceMatcher(None, table_name.lower(), tbl.lower()).ratio()
            if similarity >= threshold:
                similar_tables.append((tbl, similarity))
        
        # Sort by similarity (highest first)
        similar_tables.sort(key=lambda x: x[1], reverse=True)
        
        return [tbl for tbl, _ in similar_tables[:5]]  # Return top 5 matches
    
    except Exception as e:
        logger.error(f"Error finding similar tables: {e}")
        return []


def validate_sql(connection_string, sql_query):
    """
    Validate SQL query against database schema without executing it.
    
    Args:
        connection_string: PostgreSQL connection string
        sql_query: SQL query to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Use EXPLAIN to validate query without executing
        cursor.execute(f"EXPLAIN {sql_query}")
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def handle_sql_error(connection_string, sql_query, error):
    """
    Handle SQL execution errors with helpful feedback.
    
    Args:
        connection_string: PostgreSQL connection string
        sql_query: SQL query that caused the error
        error: The exception object or error message
        
    Returns:
        Dict containing error details and suggestions
    """
    error_msg = str(error)
    error_info = {
        "error": error_msg,
        "suggestions": [],
        "possible_fixes": []
    }
    
    # Column does not exist error
    column_match = re.search(r'column "([^"]+)" does not exist', error_msg)
    if column_match:
        column_name = column_match.group(1)
        error_info["error_type"] = "column_not_found"
        error_info["column_name"] = column_name
        
        # Try to extract table name from the query
        table_match = re.search(r'FROM\s+([^\s,]+)', sql_query, re.IGNORECASE)
        if table_match:
            table_name = table_match.group(1).strip('"')
            similar_columns = find_similar_columns(connection_string, table_name, column_name)
            
            if similar_columns:
                error_info["suggestions"].append(
                    f"Column '{column_name}' does not exist. Did you mean one of these: {', '.join(similar_columns)}?"
                )
                
                # Generate possible fixes
                for col in similar_columns:
                    fixed_query = sql_query.replace(f'"{column_name}"', f'"{col}"')
                    fixed_query = fixed_query.replace(f' {column_name} ', f' {col} ')
                    fixed_query = fixed_query.replace(f' {column_name},', f' {col},')
                    error_info["possible_fixes"].append({
                        "suggestion": f"Replace '{column_name}' with '{col}'",
                        "fixed_query": fixed_query
                    })
    
    # Table does not exist error
    table_match = re.search(r'relation "([^"]+)" does not exist', error_msg)
    if table_match:
        table_name = table_match.group(1)
        error_info["error_type"] = "table_not_found"
        error_info["table_name"] = table_name
        
        similar_tables = find_similar_tables(connection_string, table_name)
        if similar_tables:
            error_info["suggestions"].append(
                f"Table '{table_name}' does not exist. Did you mean one of these: {', '.join(similar_tables)}?"
            )
            
            # Generate possible fixes
            for tbl in similar_tables:
                fixed_query = sql_query.replace(f'"{table_name}"', f'"{tbl}"')
                fixed_query = fixed_query.replace(f' {table_name} ', f' {tbl} ')
                fixed_query = fixed_query.replace(f' {table_name},', f' {tbl},')
                error_info["possible_fixes"].append({
                    "suggestion": f"Replace '{table_name}' with '{tbl}'",
                    "fixed_query": fixed_query
                })
    
    # Syntax error
    syntax_match = re.search(r'syntax error at or near "([^"]+)"', error_msg)
    if syntax_match:
        error_token = syntax_match.group(1)
        error_info["error_type"] = "syntax_error"
        error_info["error_token"] = error_token
        error_info["suggestions"].append(
            f"Syntax error at or near '{error_token}'. Check the SQL syntax around this token."
        )
    
    # If no specific error was identified, add a generic suggestion
    if not error_info["suggestions"]:
        error_info["suggestions"].append(
            "Try reformulating your natural language query to be more specific about the tables and columns you want to query."
        )
    
    return error_info


def format_error_message(error_info):
    """
    Format error information into a user-friendly message.
    
    Args:
        error_info: Error information dictionary from handle_sql_error
        
    Returns:
        Formatted error message string
    """
    message = [
        "Error executing SQL query:",
        "-" * 50,
        error_info["error"],
        "-" * 50,
        "\nSuggestions:"
    ]
    
    for suggestion in error_info["suggestions"]:
        message.append(f"- {suggestion}")
    
    if error_info.get("possible_fixes"):
        message.append("\nPossible fixes:")
        for i, fix in enumerate(error_info["possible_fixes"], 1):
            message.append(f"{i}. {fix['suggestion']}")
    
    return "\n".join(message)
