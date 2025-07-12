import time
import sqlite3 
import functools

# Global cache dictionary
query_cache = {}

# DB connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Caching decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract query from args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query in query_cache:
            print("[CACHE] Returning cached result")
            return query_cache[query]
        print("[DB] Executing and caching query")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Function using both decorators
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call uses the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
