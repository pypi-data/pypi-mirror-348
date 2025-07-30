"""
SQL Query Generator using OpenAI.

This module provides functions to generate SQL queries from natural language
using OpenAI's language models.
"""

import os
import openai
from loguru import logger


def generate_sql_with_openai(prompt, api_key=None, model="gpt-4o-mini", temperature=0.1):
    """
    Generate SQL query using OpenAI's language models.

    Args:
        prompt: The formatted prompt for SQL generation
        api_key: OpenAI API key (optional if set in environment)
        model: OpenAI model to use (default: gpt-4o-mini)
        temperature: Sampling temperature (default: 0.1)

    Returns:
        Generated SQL query as a string or None if an error occurred
    """
    try:
        # Set API key from parameter, environment, or prompt user
        if api_key:
            openai.api_key = api_key
        elif os.getenv("OPENAI_API_KEY"):
            openai.api_key = os.getenv("OPENAI_API_KEY")
        else:
            api_key = input("Enter your OpenAI API key: ")
            os.environ["OPENAI_API_KEY"] = api_key
            openai.api_key = api_key

        # Call the OpenAI API
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert SQL query generator."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=500,
        )

        # Extract the SQL query from the response
        sql_query = response.choices[0].message.content.strip()

        # Clean up the response to extract just the SQL query
        if "```sql" in sql_query:
            # Extract content between ```sql and ```
            sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
        elif "```" in sql_query:
            # Extract content between ``` and ```
            sql_query = sql_query.split("```")[1].split("```")[0].strip()

        return sql_query

    except Exception as e:
        logger.error(f"Error generating SQL with OpenAI: {e}")
        return None
