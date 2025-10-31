seed = __import__("seed")


def stream_users():
    connection = seed.connect_to_prodev()
    if connection is None:
        return None

    cur = connection.cursor(buffered=True, dictionary=True)

    cur.execute("SELECT * FROM user_data;")
    while True:
        row = cur.fetchone()
        if row is None:
            break
        yield row
