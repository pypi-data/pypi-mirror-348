<div align="center">

# 🔍 PSQL Query Builder

<h3>Transform natural language into optimized PostgreSQL queries with AI</h3>

[![PyPI version](https://badge.fury.io/py/psql-query-builder.svg)](https://badge.fury.io/py/psql-query-builder)
[![Python Versions](https://img.shields.io/pypi/pyversions/psql-query-builder.svg)](https://pypi.org/project/psql-query-builder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/psql-query-builder)](https://pepy.tech/project/psql-query-builder)

</div>

## ✨ Overview

PSQL Query Builder is a powerful Python tool that transforms natural language into optimized PostgreSQL queries using AI. It bridges the gap between human language and SQL, making database interaction accessible to everyone - not just SQL experts.

Built on OpenAI's advanced language models, this tool analyzes your database schema and generates precise, efficient SQL queries based on plain English descriptions. Whether you're a data analyst without SQL expertise, a developer looking to speed up query writing, or a database administrator seeking to simplify access for your team, PSQL Query Builder streamlines your workflow.

## ✅ Features

<table>
  <tr>
    <td width="50%">
      <h3>🤖 AI-Powered SQL Generation</h3>
      <ul>
        <li>Transform natural language to optimized SQL</li>
        <li>Context-aware query generation</li>
        <li>Support for complex queries and joins</li>
      </ul>
    </td>
    <td width="50%">
      <h3>⚡ Smart Schema Caching</h3>
      <ul>
        <li>Automatic database schema analysis</li>
        <li>Configurable cache TTL</li>
        <li>Significant performance improvement</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🛠️ Flexible Configuration</h3>
      <ul>
        <li>Environment variables support</li>
        <li>Command-line arguments</li>
        <li>Multiple output formats (table, JSON, CSV)</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🔧 Intelligent Error Handling</h3>
      <ul>
        <li>Automatic fix suggestions</li>
        <li>Detailed error messages</li>
        <li>Interactive query correction</li>
      </ul>
    </td>
  </tr>
</table>

## 🎯 Use Cases

<div align="center">
<table>
  <tr>
    <td align="center" width="33%">
      <h3>📊 Data Analysts</h3>
      <p>Generate complex SQL queries without deep SQL knowledge</p>
      <p>Quickly explore database structures and relationships</p>
      <p>Prototype queries in natural language before refinement</p>
    </td>
    <td align="center" width="33%">
      <h3>👨‍💻 Developers</h3>
      <p>Speed up database query development</p>
      <p>Reduce time spent debugging complex SQL syntax</p>
      <p>Generate queries for unfamiliar database schemas</p>
    </td>
    <td align="center" width="33%">
      <h3>🛡️ Database Admins</h3>
      <p>Provide simplified access to non-technical team members</p>
      <p>Quickly generate queries for common reporting needs</p>
      <p>Validate schema design through natural language</p>
    </td>
  </tr>
</table>
</div>

## 🚀 Quick Start

### Installation

```bash
pip install psql-query-builder
```

### Basic Usage

```bash
# Using environment variables for connection
export PSQL_CONNECTION_STRING="postgresql://username:password@localhost:5432/database"
export OPENAI_API_KEY="your-openai-api-key"

# Run a query
psql-query-builder --query "Find all active users who registered last month"
```

### Python API

```python
from psql_query_builder import QueryBuilder

# Initialize the query builder
builder = QueryBuilder(
    connection_string="postgresql://username:password@localhost:5432/database",
    openai_api_key="your-openai-api-key"
)

# Generate and execute a query
results = builder.run_query(
    "Find all products with more than 100 units in stock and price less than $50",
    execute=True
)

# Print the results
print(results)
```

### LangChain Integration

PSQL Query Builder can be easily integrated with LangChain to enable natural language database queries in your AI applications:

```python
# Using the @tool decorator approach
from langchain_core.tools import tool

@tool
def query_database(query: str, connection_string: str = "postgresql://user:pass@localhost/db"):
    """Execute a natural language query against a PostgreSQL database."""
    from psql_query_builder import QueryBuilder
    
    builder = QueryBuilder(connection_string=connection_string)
    return builder.run_query(query, execute=True)

# Use with LangChain
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor

llm = ChatOpenAI(model="gpt-4-turbo")
tools = [query_database]
agent = create_openai_tools_agent(llm, tools, prompt=None)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Run the agent
response = agent_executor.invoke({"input": "Find all users who registered last month"})
print(response["output"])
```

For more advanced integration options, see the full documentation.

## ⚙️ Configuration

<details>
<summary><b>Environment Variables</b></summary>

```bash
# Full connection string
export PSQL_CONNECTION_STRING="postgresql://username:password@localhost:5432/database"

# Or individual connection parameters
export PSQL_HOST="localhost"
export PSQL_PORT="5432"
export PSQL_USER="username"
export PSQL_PASSWORD="password"
export PSQL_DATABASE="database"

# OpenAI API key
export OPENAI_API_KEY="your-openai-api-key"
```
</details>

<details>
<summary><b>Command-line Arguments</b></summary>

```bash
psql-query-builder \
  --host localhost \
  --port 5432 \
  --user username \
  --password password \
  --database database \
  --api-key your-openai-api-key \
  --query "Find all products with more than 100 units in stock" \
  --dry-run  # Optional: generate SQL without executing
```
</details>

<details>
<summary><b>Dry Run Mode</b></summary>

```bash
# Generate SQL only, don't execute (useful for reviewing queries before running on production databases)
psql-query-builder --query "Find all inactive users who haven't logged in for 3 months" --dry-run

# Output:
# Generated SQL query (dry run mode):
# --------------------------------------------------
# SELECT u.id, u.username, u.email, u.last_login
# FROM users u
# WHERE u.last_login < NOW() - INTERVAL '3 months'
# ORDER BY u.last_login ASC;
# --------------------------------------------------
```
</details>

<details>
<summary><b>Schema Caching</b></summary>

For better performance with repeated queries, enable schema caching:

```bash
# Enable schema caching with default settings
psql-query-builder --query "Find all users who placed orders in the last week" --cache

# Specify cache path and TTL (time-to-live in seconds)
psql-query-builder --query "Find all users who placed orders in the last week" \
  --cache \
  --cache-path "/tmp/schema_cache" \
  --cache-ttl 3600

# Force refresh the cache
psql-query-builder --query "Find all users who placed orders in the last week" \
  --cache \
  --force-refresh
```
</details>

## 📘 Advanced Usage

<div align="center">
<table>
  <tr>
    <td align="center" width="50%">
      <h3>💬 Interactive Mode</h3>
      <p>Start an interactive session for multiple queries:</p>
      <pre><code>psql-query-builder</code></pre>
      <p>Then enter queries at the prompt:</p>
      <pre><code>> Find all customers in California
> Show revenue by product category
> exit</code></pre>
    </td>
    <td align="center" width="50%">
      <h3>🔍 Single Query Mode</h3>
      <p>Execute a single query and exit:</p>
      <pre><code>psql-query-builder --query "Find all users 
who registered in the last month"</code></pre>
      <p>Perfect for scripts and automation</p>
    </td>
  </tr>
</table>
</div>

## 📚 API Reference

<details>
<summary><b>Python API</b></summary>

```python
from psql_query_builder import QueryBuilder

# Initialize with connection string
builder = QueryBuilder(
    connection_string="postgresql://username:password@localhost:5432/database",
    openai_api_key="your-openai-api-key"
)

# Or with individual parameters
builder = QueryBuilder(
    host="localhost",
    port=5432,
    database="mydatabase",
    user="myuser",
    password="mypassword",
    openai_api_key="your-openai-api-key"
)

# Generate SQL without executing
sql = builder.generate_query("Find all users who registered last month")
print(sql)

# Generate and execute query
results = builder.run_query(
    "Find all products with more than 100 units in stock",
    execute=True
)
print(results)
```
</details>

## 🚩 Roadmap

Future development plans for PSQL Query Builder include:

- [ ] Support for more database systems (MySQL, SQLite, SQL Server)
- [ ] Interactive SQL editing and refinement
- [ ] Query history management and reuse
- [ ] Integration with popular database tools and ORMs
- [ ] Web interface for non-CLI usage
- [ ] Query optimization suggestions
- [ ] Support for database migrations and schema changes

Feel free to contribute to any of these features or suggest new ones!

## 👨‍💻 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs or request features**: Open an issue describing what you found or what you'd like to see
2. **Submit improvements**: Fork the repository, make your changes, and submit a pull request
3. **Improve documentation**: Help clarify or expand the documentation
4. **Share your use cases**: Let us know how you're using PSQL Query Builder

## 📜 License

MIT
