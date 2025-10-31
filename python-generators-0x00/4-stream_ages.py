seed = __import__("seed")


def stream_user_ages():
    connection = seed.connect_to_prodev()
    cur = connection.cursor(buffered=True)
    cur.execute("SELECT age from user_data;")
    while True:
        age = cur.fetchone()
        if age is None:
            break
        yield int(age[0])


def print_average_age():
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    print(f"Average age of users: {total / count}")


print_average_age()
