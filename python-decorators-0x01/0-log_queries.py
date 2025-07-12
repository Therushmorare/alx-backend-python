import sqlite3
import functools

# Decorator to log SQL queries
def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Try to extract the SQL query
            query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
            if query:
                print(f"[SQL LOG] Executing query: {query}")
            else:
                print("[SQL LOG] No query found to log.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Function that runs a query
@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Call the function
users = fetch_all_users(query="SELECT * FROM users")
