"""
Database interaction module for PSQL Query Builder.

This module provides functions to interact with PostgreSQL databases,
including retrieving database schema information and executing queries.
"""

from urllib.parse import urlparse, parse_qs
import psycopg2
from psycopg2 import sql
from loguru import logger


def parse_postgres_url(url: str) -> dict:
    """
    Parse a PostgreSQL connection URL into its components.
    
    Args:
        url: PostgreSQL connection URL in the format:
             postgresql://username:password@host:port/dbname?param=value
    
    Returns:
        Dictionary containing the connection parameters
    """
    result = {}
    
    # Use urlparse to break down the URL
    parsed = urlparse(url)
    
    # Extract username and password
    if '@' in parsed.netloc:
        userpass, hostport = parsed.netloc.split('@', 1)
        if ':' in userpass:
            result['user'], result['password'] = userpass.split(':', 1)
        else:
            result['user'] = userpass
    else:
        hostport = parsed.netloc
    
    # Extract host and port
    if ':' in hostport:
        result['host'], result['port'] = hostport.split(':', 1)
    else:
        result['host'] = hostport
    
    # Extract database name
    path = parsed.path
    if path.startswith('/'):
        path = path[1:]  # Remove leading slash
    result['dbname'] = path
    
    # Extract query parameters
    query_params = parse_qs(parsed.query)
    for key, values in query_params.items():
        result[key] = values[0]  # Take the first value for each parameter
    
    return result


def get_database_summary(connection_string: str) -> str:
    """
    Generate a summary overview of a PostgreSQL database structure.
    
    Args:
        connection_string: PostgreSQL connection URL
    
    Returns:
        A formatted string containing the database summary
    """
    try:
        # Parse the connection string and use it for connection
        conn_params = parse_postgres_url(connection_string)
        
        # Connect to the database
        conn = psycopg2.connect(
            dbname=conn_params.get('dbname', ''),
            user=conn_params.get('user', 'postgres'),
            password=conn_params.get('password', ''),
            host=conn_params.get('host', 'localhost'),
            port=conn_params.get('port', '5432'),
            sslmode=conn_params.get('sslmode', 'prefer')
        )
        
        dbname = conn_params.get('dbname', 'unknown')
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Initialize summary
        summary = [f"DATABASE SUMMARY: {dbname}\n"]
        summary.append("=" * 50 + "\n")
        
        # Get schemas
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
            ORDER BY schema_name
        """)
        schemas = [row[0] for row in cursor.fetchall()]
        
        summary.append(f"SCHEMAS ({len(schemas)}):\n")
        for schema in schemas:
            summary.append(f"  - {schema}\n")
        
        summary.append("\n")
        
        # For each schema, get tables and views
        for schema in schemas:
            # Get tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = %s
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """, (schema,))
            tables = [row[0] for row in cursor.fetchall()]
            
            if tables:
                summary.append(f"SCHEMA: {schema} - TABLES ({len(tables)}):\n")
                
                # For each table, get columns and constraints
                for table in tables:
                    # Get column information
                    cursor.execute("""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_schema = %s AND table_name = %s
                        ORDER BY ordinal_position
                    """, (schema, table))
                    columns = cursor.fetchall()
                    
                    # Get primary key information
                    cursor.execute("""
                        SELECT kcu.column_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                            ON tc.constraint_name = kcu.constraint_name
                            AND tc.table_schema = kcu.table_schema
                        WHERE tc.constraint_type = 'PRIMARY KEY'
                            AND tc.table_schema = %s
                            AND tc.table_name = %s
                    """, (schema, table))
                    primary_keys = [row[0] for row in cursor.fetchall()]
                    
                    # Get foreign key information
                    cursor.execute("""
                        SELECT
                            kcu.column_name,
                            ccu.table_schema AS foreign_table_schema,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                            ON tc.constraint_name = kcu.constraint_name
                            AND tc.table_schema = kcu.table_schema
                        JOIN information_schema.constraint_column_usage ccu
                            ON ccu.constraint_name = tc.constraint_name
                            AND ccu.table_schema = tc.table_schema
                        WHERE tc.constraint_type = 'FOREIGN KEY'
                          AND tc.table_schema = %s
                          AND tc.table_name = %s
                    """, (schema, table))
                    foreign_keys = cursor.fetchall()
                    
                    # Get approximate row count
                    try:
                        cursor.execute(sql.SQL("""
                            SELECT COUNT(*) FROM {}.{}
                        """).format(
                            sql.Identifier(schema),
                            sql.Identifier(table)
                        ))
                        row_count = cursor.fetchone()[0]
                    except Exception:
                        row_count = "N/A"
                    
                    # Add table info to summary
                    summary.append(f"  - Table: {table} (~ {row_count} rows)\n")
                    
                    if primary_keys:
                        summary.append(f"    PK: {', '.join(primary_keys)}\n")
                    
                    summary.append("    Columns:\n")
                    for col_name, data_type, is_nullable in columns:
                        nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                        summary.append(f"      {col_name} ({data_type}, {nullable})\n")
                    
                    if foreign_keys:
                        summary.append("    Foreign Keys:\n")
                        for col, f_schema, f_table, f_col in foreign_keys:
                            summary.append(f"      {col} -> {f_schema}.{f_table}.{f_col}\n")
                    
                    summary.append("\n")
            
            # Get views
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.views 
                WHERE table_schema = %s
                ORDER BY table_name
            """, (schema,))
            views = [row[0] for row in cursor.fetchall()]
            
            if views:
                summary.append(f"SCHEMA: {schema} - VIEWS ({len(views)}):\n")
                for view in views:
                    summary.append(f"  - {view}\n")
                summary.append("\n")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return "".join(summary)
    
    except Exception as e:
        return f"Error generating database summary: {str(e)}"


def run_query(conn_str, query):
    """
    Execute a SQL query against a PostgreSQL database.
    
    Args:
        conn_str: PostgreSQL connection string
        query: SQL query to execute
        
    Returns:
        List of result rows or None if an error occurred
    """
    retrieved_results = []
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            retrieved_results.append(row)
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return None
    
    return retrieved_results
