import sqlite3
import functools

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection as first argument
            return result
        finally:
            conn.close()  # Always close connection
    return wrapper

# Decorated function with automatic connection handling
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Usage
user = get_user_by_id(user_id=1)
print(user)
