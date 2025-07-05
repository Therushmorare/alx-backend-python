import mysql.connector
seed = __import__('seed')

def stream_user_ages():
    """Generator that yields ages of users one by one."""
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:   # loop 1
        yield row['age']

    cursor.close()
    conn.close()

def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():  # loop 2
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
    else:
        average = 0

    print(f"Average age of users: {average}")

if __name__ == "__main__":
    calculate_average_age()
