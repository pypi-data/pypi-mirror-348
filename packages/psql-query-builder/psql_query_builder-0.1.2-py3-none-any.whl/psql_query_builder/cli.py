"""
Command Line Interface for PSQL Query Builder.

This module provides a command-line interface for generating and executing
SQL queries from natural language using the PSQL Query Builder.
"""

import os
import sys
import argparse
import json
from tabulate import tabulate
from loguru import logger

from .db_agent import run_query
from .prompt import generate_sql_prompt
from .query_generator import generate_sql_with_openai
from .schema_cache import get_cached_schema, clear_schema_cache
from .error_handler import validate_sql, handle_sql_error, format_error_message
from . import __version__


def configure_logger(verbose=False):
    """Configure the logger based on verbosity level."""
    logger.remove()  # Remove default handler
    level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=level)


def get_connection_string(args):
    """
    Get the database connection string from args or environment variables.
    
    Priority order:
    1. Command line argument
    2. Environment variable
    3. Prompt user for input
    """
    if args.connection_string:
        return args.connection_string
    
    # Check individual connection parameters
    if all([args.host, args.dbname, args.user]):
        # Build connection string from individual parameters
        conn_str = f"postgresql://{args.user}"
        if args.password:
            conn_str += f":{args.password}"
        conn_str += f"@{args.host}"
        if args.port:
            conn_str += f":{args.port}"
        conn_str += f"/{args.dbname}"
        if args.sslmode:
            conn_str += f"?sslmode={args.sslmode}"
        return conn_str
    
    # Check environment variables
    if os.getenv("PSQL_CONNECTION_STRING"):
        return os.getenv("PSQL_CONNECTION_STRING")
    
    # Build from individual environment variables
    if all([os.getenv("PSQL_HOST"), os.getenv("PSQL_DBNAME"), os.getenv("PSQL_USER")]):
        conn_str = f"postgresql://{os.getenv('PSQL_USER')}"
        if os.getenv("PSQL_PASSWORD"):
            conn_str += f":{os.getenv('PSQL_PASSWORD')}"
        conn_str += f"@{os.getenv('PSQL_HOST')}"
        if os.getenv("PSQL_PORT"):
            conn_str += f":{os.getenv('PSQL_PORT')}"
        conn_str += f"/{os.getenv('PSQL_DBNAME')}"
        if os.getenv("PSQL_SSLMODE"):
            conn_str += f"?sslmode={os.getenv('PSQL_SSLMODE')}"
        return conn_str
    
    # Prompt user for connection string
    return input("Enter PostgreSQL connection string (postgresql://user:password@host:port/dbname):\n")


def get_openai_api_key(args):
    """
    Get the OpenAI API key from args or environment variables.
    
    Priority order:
    1. Command line argument
    2. Environment variable
    3. Prompt user for input (handled by generate_sql_with_openai)
    """
    if args.openai_api_key:
        return args.openai_api_key
    return os.getenv("OPENAI_API_KEY")


def display_results(results, output_format="table"):
    """
    Display query results in the specified format.
    
    Args:
        results: Query results from run_query
        output_format: Format to display results (table, json, csv)
    """
    if not results:
        print("No results returned.")
        return
    
    if output_format == "json":
        # Convert to list of dictionaries for better JSON representation
        print(json.dumps(results, indent=2, default=str))
    elif output_format == "csv":
        # Simple CSV output
        for row in results:
            print(",".join(str(col) for col in row))
    else:  # Default to table
        # Assume first row has same structure as all rows
        headers = [f"Column {i+1}" for i in range(len(results[0]))]
        print(tabulate(results, headers=headers, tablefmt="psql"))


def interactive_mode(args):
    """Run the query builder in interactive mode."""
    connection_string = get_connection_string(args)
    openai_api_key = get_openai_api_key(args)
    
    # Handle schema cache clearing if requested
    if args.clear_schema_cache:
        count = clear_schema_cache(connection_string, args.schema_cache_path)
        logger.info(f"Cleared {count} schema cache files")
    
    # Get database summary with caching
    logger.info("Getting database schema...")
    summary = get_cached_schema(
        connection_string=connection_string,
        cache_path=args.schema_cache_path,
        ttl=args.schema_cache_ttl,
        force_refresh=args.refresh_schema
    )
    logger.debug(summary)

    print("\n" + "=" * 50)
    print("Database summary loaded. You can now enter queries.")
    print("Type 'exit' or 'quit' to end the program.")
    print("=" * 50 + "\n")

    # Main loop for processing queries
    while True:
        # get user natural language query
        user_query = input("\nEnter your natural language query (or 'exit' to quit):\n")

        # Check if user wants to exit
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting program. Goodbye!")
            break

        # generate sql prompt
        logger.info("Generating SQL prompt...")
        prompt = generate_sql_prompt(user_query, summary, include_examples=not args.no_examples)
        logger.debug(prompt)

        # generate SQL query using OpenAI
        logger.info("Generating SQL query with OpenAI...")
        sql_query = generate_sql_with_openai(
            prompt, 
            api_key=openai_api_key,
            model=args.model,
            temperature=args.temperature
        )

        if sql_query:
            logger.info(f"Generated SQL query:\n{sql_query}")
            
            # Validate the SQL query against the schema
            is_valid, error_message = validate_sql(connection_string, sql_query)
            if not is_valid:
                error_info = handle_sql_error(connection_string, sql_query, error_message)
                print(format_error_message(error_info))
                
                # Ask if user wants to continue despite validation error
                continue_anyway = input("\nContinue with execution anyway? (y/n): ").lower() == 'y'
                if not continue_anyway:
                    continue
            
            if args.dry_run:
                print("\nGenerated SQL query (dry run mode):")
                print("-" * 50)
                print(sql_query)
                print("-" * 50)
                continue
            
            # run query
            logger.info("Running query...")
            try:
                results = run_query(connection_string, sql_query)

                # Display results
                if results is not None:
                    print("\nQuery results:")
                    print("-" * 50)
                    display_results(results, args.output_format)
                    print("-" * 50)
                else:
                    logger.error("Query execution failed.")
            except Exception as e:
                error_info = handle_sql_error(connection_string, sql_query, e)
                print(format_error_message(error_info))
                
                if error_info.get("possible_fixes") and len(error_info["possible_fixes"]) > 0:
                    fix_option = input(f"\nApply a fix? (1-{len(error_info['possible_fixes'])}, or 'n' to skip): ")
                    if fix_option.isdigit() and 1 <= int(fix_option) <= len(error_info["possible_fixes"]):
                        fixed_idx = int(fix_option) - 1
                        fixed_query = error_info["possible_fixes"][fixed_idx]["fixed_query"]
                        print(f"\nTrying fixed query:\n{fixed_query}")
                        try:
                            results = run_query(connection_string, fixed_query)
                            if results is not None:
                                print("\nQuery results (with fix):")
                                print("-" * 50)
                                display_results(results, args.output_format)
                                print("-" * 50)
                            else:
                                logger.error("Fixed query execution failed.")
                        except Exception as e2:
                            logger.error(f"Error with fixed query: {e2}")
        else:
            logger.error("Failed to generate SQL query.")


def single_query_mode(args):
    """Run a single query and exit."""
    if not args.query:
        logger.error("No query provided for single query mode. Use --query or -q option.")
        sys.exit(1)
    
    connection_string = get_connection_string(args)
    openai_api_key = get_openai_api_key(args)
    
    # Handle schema cache clearing if requested
    if args.clear_schema_cache:
        count = clear_schema_cache(connection_string, args.schema_cache_path)
        logger.info(f"Cleared {count} schema cache files")
    
    # Get database summary with caching
    logger.info("Getting database schema...")
    summary = get_cached_schema(
        connection_string=connection_string,
        cache_path=args.schema_cache_path,
        ttl=args.schema_cache_ttl,
        force_refresh=args.refresh_schema
    )
    logger.debug(summary)
    
    # Generate SQL prompt
    logger.info("Generating SQL prompt...")
    prompt = generate_sql_prompt(args.query, summary, include_examples=not args.no_examples)
    logger.debug(prompt)
    
    # Generate SQL query
    logger.info("Generating SQL query with OpenAI...")
    sql_query = generate_sql_with_openai(
        prompt, 
        api_key=openai_api_key,
        model=args.model,
        temperature=args.temperature
    )
    
    if sql_query:
        logger.info(f"Generated SQL query:\n{sql_query}")
        
        # Validate the SQL query against the schema
        is_valid, error_message = validate_sql(connection_string, sql_query)
        if not is_valid:
            error_info = handle_sql_error(connection_string, sql_query, error_message)
            print(format_error_message(error_info))
            
            # Ask if user wants to continue despite validation error
            continue_anyway = input("\nContinue with execution anyway? (y/n): ").lower() == 'y'
            if not continue_anyway:
                sys.exit(1)
        
        if args.dry_run:
            print("\nGenerated SQL query (dry run mode):")
            print("-" * 50)
            print(sql_query)
            print("-" * 50)
            return
        
        # Run query
        logger.info("Running query...")
        try:
            results = run_query(connection_string, sql_query)
            
            # Display results
            if results is not None:
                print("\nQuery results:")
                print("-" * 50)
                display_results(results, args.output_format)
                print("-" * 50)
            else:
                logger.error("Query execution failed.")
        except Exception as e:
            error_info = handle_sql_error(connection_string, sql_query, e)
            print(format_error_message(error_info))
            
            if error_info.get("possible_fixes") and len(error_info["possible_fixes"]) > 0:
                fix_option = input(f"\nApply a fix? (1-{len(error_info['possible_fixes'])}, or 'n' to skip): ")
                if fix_option.isdigit() and 1 <= int(fix_option) <= len(error_info["possible_fixes"]):
                    fixed_idx = int(fix_option) - 1
                    fixed_query = error_info["possible_fixes"][fixed_idx]["fixed_query"]
                    print(f"\nTrying fixed query:\n{fixed_query}")
                    try:
                        results = run_query(connection_string, fixed_query)
                        if results is not None:
                            print("\nQuery results (with fix):")
                            print("-" * 50)
                            display_results(results, args.output_format)
                            print("-" * 50)
                        else:
                            logger.error("Fixed query execution failed.")
                    except Exception as e2:
                        logger.error(f"Error with fixed query: {e2}")
    else:
        logger.error("Failed to generate SQL query.")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="PSQL Query Builder - Generate and execute SQL queries from natural language"
    )
    
    # Version information
    parser.add_argument(
        "--version", "-v", action="version", 
        version=f"PSQL Query Builder v{__version__}"
    )
    
    # Verbosity
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose output"
    )
    
    # Database connection options
    db_group = parser.add_argument_group("Database Connection Options")
    db_group.add_argument(
        "--connection-string", "-c",
        help="PostgreSQL connection string (postgresql://user:password@host:port/dbname)"
    )
    db_group.add_argument("--host", help="Database host")
    db_group.add_argument("--port", help="Database port")
    db_group.add_argument("--dbname", help="Database name")
    db_group.add_argument("--user", help="Database user")
    db_group.add_argument("--password", help="Database password")
    db_group.add_argument(
        "--sslmode", 
        choices=["disable", "allow", "prefer", "require", "verify-ca", "verify-full"],
        help="SSL mode for database connection"
    )
    
    # Schema cache options
    cache_group = parser.add_argument_group("Schema Cache Options")
    cache_group.add_argument(
        "--schema-cache-path",
        help="Path to store schema cache files (default: ~/.psql_query_builder/schema_cache)"
    )
    cache_group.add_argument(
        "--schema-cache-ttl", type=int, default=86400,
        help="Schema cache time-to-live in seconds (default: 86400, i.e., 24 hours)"
    )
    cache_group.add_argument(
        "--refresh-schema", action="store_true",
        help="Force refresh of schema cache"
    )
    cache_group.add_argument(
        "--clear-schema-cache", action="store_true",
        help="Clear schema cache before running"
    )
    
    # OpenAI options
    openai_group = parser.add_argument_group("OpenAI Options")
    openai_group.add_argument(
        "--openai-api-key", "-k",
        help="OpenAI API key (if not set in OPENAI_API_KEY environment variable)"
    )
    openai_group.add_argument(
        "--model", "-m", default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini)"
    )
    openai_group.add_argument(
        "--temperature", "-t", type=float, default=0.1,
        help="Temperature for OpenAI API (default: 0.1)"
    )
    openai_group.add_argument(
        "--no-examples", action="store_true",
        help="Don't include example queries in the prompt"
    )
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "--output-format", "-o", 
        choices=["table", "json", "csv"], default="table",
        help="Output format for query results (default: table)"
    )
    output_group.add_argument(
        "--dry-run", "-d", action="store_true",
        help="Generate SQL but don't execute it"
    )
    
    # Query mode
    parser.add_argument(
        "--query", "-q",
        help="Natural language query (if provided, runs in single query mode)"
    )
    
    args = parser.parse_args()
    
    # Configure logger
    configure_logger(args.verbose)
    
    # Run in appropriate mode
    if args.query:
        single_query_mode(args)
    else:
        interactive_mode(args)


if __name__ == "__main__":
    main()
