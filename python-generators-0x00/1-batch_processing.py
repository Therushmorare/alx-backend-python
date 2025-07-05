import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows (lists of dicts) from user_data.
    Each batch contains up to batch_size users.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # update as needed
        password="",       # update as needed
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    batch = []
    for row in cursor:                 # loop 1
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
    Processes each batch yielded by stream_users_in_batches.
    Filters users over the age of 25 and yields them one by one.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:                             # loop 3
            if user['age'] > 25:
                print(user)
