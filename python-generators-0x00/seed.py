import mysql.connector
import uuid
import csv

def connect_db():
    """Connects to MySQL server (no DB specified)."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # change if needed
            password=""       # change if needed
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create database ALX_prodev if not exists."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",     # change if needed
            password="",     # change if needed
            database="ALX_prodev"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table if not exists."""
    cursor = connection.cursor()

    # Read CSV
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row.get('user_id') or str(uuid.uuid4())  # use CSV user_id or generate new UUID
            name = row['name']
            email = row['email']
            age = row['age']

            # Check if user_id exists
            cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (user_id,))
            if cursor.fetchone():
                continue  # Skip existing record

            # Insert new record
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, name, email, age))

    connection.commit()
    cursor.close()
