import mysql.connector

def stream_users():
    """Generator to fetch user_data rows one by one as dicts."""
    # Connect to the ALX_prodev database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # update as needed
        password="",       # update as needed
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)  # return rows as dicts
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    
    for row in cursor:
        yield row

    cursor.close()
    conn.close()
