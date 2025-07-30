# PSQL Query Builder

Generate PostgreSQL queries from natural language using AI.

## Overview

PSQL Query Builder is a Python tool that allows you to generate SQL queries for PostgreSQL databases using natural language. It leverages OpenAI's language models to translate your plain English requests into proper SQL queries, making database interaction more accessible.

## Features

- Generate SQL queries from natural language descriptions
- Automatic database schema analysis with smart caching
- Enhanced error handling with automatic fix suggestions
- Execute generated queries and display results
- Flexible configuration via environment variables or command-line arguments
- Interactive mode for multiple queries
- Single query mode for scripting

## Installation

```bash
pip install psql-query-builder
```

## Quick Start

Here's how to get started with PSQL Query Builder in just a few steps:

1. **Install the package**:
   ```bash
   pip install psql-query-builder
   ```

2. **Set up your database connection** (choose one):
   - Using command line: `psql-query-builder --connection-string "postgresql://user:password@host:port/dbname"`
   - Using environment variables: Copy `.env.example` to `.env`, edit with your details, then run `psql-query-builder`

3. **Ask questions in natural language**:
   ```
   Enter your natural language query:
   > Show me all users who registered in the last month
   ```

4. **Get SQL and results**:
   The tool will generate the SQL query and execute it, showing you the results.

## Usage

### Command Line Interface

The package provides a command-line interface with two modes of operation:

#### Interactive Mode

```bash
# Basic usage with connection string
psql-query-builder --connection-string "postgresql://user:password@host:port/dbname"

# Using individual connection parameters
psql-query-builder --host localhost --port 5432 --dbname mydb --user myuser --password mypassword

# Using environment variables (set PSQL_CONNECTION_STRING or individual PSQL_* variables)
psql-query-builder
```

#### Single Query Mode

```bash
# Run a single query and exit
psql-query-builder --query "Show me all users who signed up last month" --output-format json

# Generate SQL without executing it (dry run mode)
psql-query-builder --query "List all products with price greater than 100" --dry-run
```

### Configuration Options

#### Environment Variables

A sample `.env.example` file is included in the package. You can copy this file to `.env` and update it with your values:

```bash
# Copy the example file to .env
cp .env.example .env

# Edit the .env file with your values
vim .env  # or use any text editor
```

#### Database Connection

You can configure the database connection in several ways (in order of precedence):

1. Command-line arguments:
   ```
   --connection-string "postgresql://user:password@host:port/dbname"
   ```
   
   Or individual parameters:
   ```
   --host localhost --port 5432 --dbname mydb --user myuser --password mypassword --sslmode require
   ```

2. Environment variables (in `.env` file or exported to your shell):
   ```
   PSQL_CONNECTION_STRING="postgresql://user:password@host:port/dbname"
   ```
   
   Or individual variables:
   ```
   PSQL_HOST=localhost
   PSQL_PORT=5432
   PSQL_DBNAME=mydb
   PSQL_USER=myuser
   PSQL_PASSWORD=mypassword
   PSQL_SSLMODE=require
   ```

3. Interactive prompt if no connection details are provided

#### Schema Caching

The tool includes a smart schema caching system that significantly improves performance when running multiple queries against the same database. Key features include:

- Automatic caching of database schema information
- Configurable cache time-to-live (TTL)
- Options to force refresh or clear the cache

To use schema caching options:

```bash
# Specify custom cache location
psql-query-builder --schema-cache-path ~/.cache/psql-query-builder

# Set custom TTL (in seconds, default is 24 hours)
psql-query-builder --schema-cache-ttl 3600

# Force refresh the schema cache
psql-query-builder --refresh-schema

# Clear the schema cache before running
psql-query-builder --clear-schema-cache
```

Schema caching is particularly useful for large databases where schema analysis can take significant time.

#### Enhanced Error Handling

The tool provides intelligent error handling with helpful suggestions when SQL queries fail:

- Detailed error messages with context
- Automatic suggestions for fixing common errors
- Interactive fix application for quick recovery
- Support for column and table name typos

When a query fails, the tool will:

1. Analyze the error to determine the cause
2. Suggest possible fixes based on the database schema
3. Allow you to apply a fix and retry the query

This makes the tool much more user-friendly, especially for those who are not SQL experts.

#### Dry Run Mode

Dry run mode allows you to generate SQL queries without executing them. This is useful for:

- Reviewing and validating generated SQL before execution
- Learning how the tool translates natural language to SQL
- Debugging or troubleshooting query generation
- Saving queries for later execution

To use dry run mode, add the `--dry-run` or `-d` flag:

```bash
psql-query-builder --query "Find all transactions over $1000" --dry-run
```

The tool will connect to your database to analyze the schema, generate the SQL query using OpenAI, and then display the query without executing it. This is particularly helpful when working with production databases where you want to review queries before running them.

#### OpenAI API

Configure the OpenAI API:

1. Command-line arguments:
   ```
   --openai-api-key "your-api-key"
   --model "gpt-4o-mini"
   --temperature 0.1
   ```

2. Environment variables:
   ```
   OPENAI_API_KEY="your-api-key"
   ```

3. Interactive prompt if API key is not provided

### Python API

You can also use PSQL Query Builder as a library in your Python code:

```python
from psql_query_builder import get_database_summary, generate_sql_prompt, generate_sql_with_openai, run_query

# Get database schema
connection_string = "postgresql://user:password@host:port/dbname"
db_schema = get_database_summary(connection_string)

# Generate SQL from natural language
user_query = "Show me all active users who registered in the last month"
prompt = generate_sql_prompt(user_query, db_schema)
sql_query = generate_sql_with_openai(prompt)

# Execute the query
results = run_query(connection_string, sql_query)
print(results)
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
