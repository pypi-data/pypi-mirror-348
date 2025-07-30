"""
Schema caching module for PSQL Query Builder.

This module provides functionality to cache database schema information
to improve performance for repeated queries.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from loguru import logger


# Default cache TTL (24 hours in seconds)
DEFAULT_CACHE_TTL = 86400


def get_default_cache_path():
    """Get the default path for schema cache files."""
    cache_dir = Path.home() / ".psql_query_builder" / "schema_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_key(connection_string):
    """
    Generate a unique cache key for a connection string.
    
    This creates a deterministic but anonymized key based on the connection details.
    """
    import hashlib
    # Create a hash of the connection string to use as the filename
    # This avoids exposing sensitive connection details in the cache filename
    return hashlib.md5(connection_string.encode()).hexdigest()


def get_cached_schema(connection_string, cache_path=None, ttl=None, force_refresh=False):
    """
    Get database schema with caching support.
    
    Args:
        connection_string: PostgreSQL connection string
        cache_path: Path to store the schema cache (default: ~/.psql_query_builder/schema_cache)
        ttl: Cache time-to-live in seconds (default: 24 hours)
        force_refresh: Whether to force a refresh of the cache
        
    Returns:
        The database schema as a string
    """
    from .db_agent import get_database_summary
    
    # Set defaults
    if cache_path is None:
        cache_path = get_default_cache_path()
    else:
        cache_path = Path(cache_path)
        cache_path.mkdir(parents=True, exist_ok=True)
    
    if ttl is None:
        ttl = DEFAULT_CACHE_TTL
    
    # Generate cache filename from connection string
    cache_key = get_cache_key(connection_string)
    cache_file = cache_path / f"{cache_key}.json"
    
    # Check if we have a valid cached schema
    if not force_refresh and cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            cache_age = time.time() - cached_time.timestamp()
            
            if cache_age < ttl:
                logger.debug(f"Using cached schema (age: {cache_age:.1f}s)")
                return cache_data['schema']
            else:
                logger.debug(f"Cache expired (age: {cache_age:.1f}s)")
        except Exception as e:
            logger.warning(f"Error reading cache file: {e}")
    
    # Generate fresh schema
    logger.info("Generating fresh database schema...")
    schema = get_database_summary(connection_string)
    
    # Cache the schema
    try:
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'schema': schema
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        logger.debug(f"Schema cached to {cache_file}")
    except Exception as e:
        logger.warning(f"Error writing cache file: {e}")
    
    return schema


def clear_schema_cache(connection_string=None, cache_path=None):
    """
    Clear schema cache files.
    
    Args:
        connection_string: If provided, clear only the cache for this connection
        cache_path: Path to the schema cache directory
        
    Returns:
        Number of cache files removed
    """
    if cache_path is None:
        cache_path = get_default_cache_path()
    else:
        cache_path = Path(cache_path)
    
    count = 0
    
    if connection_string:
        # Clear specific cache file
        cache_key = get_cache_key(connection_string)
        cache_file = cache_path / f"{cache_key}.json"
        
        if cache_file.exists():
            cache_file.unlink()
            count = 1
    else:
        # Clear all cache files
        for cache_file in cache_path.glob("*.json"):
            cache_file.unlink()
            count += 1
    
    return count
