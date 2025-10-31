import mysql.connector

seed = __import__("seed")


def stream_users_in_batches(batch_size: int):
    try:
        connection = seed.connect_to_prodev()

        cur = connection.cursor(buffered=True, dictionary=True)
        offset = 0

        while True:
            cur.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s;", (batch_size, offset)
            )
            rows = cur.fetchall()
            if not rows:
                break
            yield rows
            offset += batch_size
        cur.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"database error: {e}")
    except Exception as e:
        print(f"error processing: {e}")


def batch_processing(batch_size: int):
    for batch in stream_users_in_batches(batch_size=batch_size):
        for user in batch:
            if int(user["age"]) > 25:
                print(user)
