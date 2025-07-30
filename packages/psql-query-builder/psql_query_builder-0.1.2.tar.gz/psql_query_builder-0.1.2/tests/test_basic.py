"""
Basic tests for PSQL Query Builder.
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from psql_query_builder import generate_sql_prompt, parse_postgres_url


class TestPSQLQueryBuilder(unittest.TestCase):
    """Basic tests for PSQL Query Builder."""

    def test_parse_postgres_url(self):
        """Test parsing PostgreSQL connection URL."""
        url = "postgresql://user:pass@localhost:5432/testdb?sslmode=require"
        result = parse_postgres_url(url)
        
        self.assertEqual(result["user"], "user")
        self.assertEqual(result["password"], "pass")
        self.assertEqual(result["host"], "localhost")
        self.assertEqual(result["port"], "5432")
        self.assertEqual(result["dbname"], "testdb")
        self.assertEqual(result["sslmode"], "require")

    def test_generate_sql_prompt(self):
        """Test generating SQL prompt."""
        user_query = "Show me all users"
        db_schema = "DATABASE SUMMARY: testdb\n==================================================\n"
        prompt = generate_sql_prompt(user_query, db_schema, include_examples=False)
        
        self.assertIn("You are an expert PostgreSQL query generator", prompt)
        self.assertIn("DATABASE SUMMARY: testdb", prompt)
        self.assertIn("Show me all users", prompt)


if __name__ == "__main__":
    unittest.main()
