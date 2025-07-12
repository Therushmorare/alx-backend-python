import sqlite3

# Custom context manager class
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # this is passed to the `as` variable

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"[ERROR] {exc_type}: {exc_value}")
        # Returning False will re-raise the exception if it occurred
        return False

# Use the context manager to fetch users
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
