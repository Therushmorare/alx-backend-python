import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches of batch_size.
    Each batch is a list of dicts.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # update if needed
        password="",       # update if needed
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    batch = []
    for row in cursor:              # loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """
    Processes batches from stream_users_in_batches.
    Yields users with age > 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:                              # loop 3
            if user['age'] > 25:
                yield user
