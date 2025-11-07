import sqlite3
import functools


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        result = func(conn, *args, **kwargs)
        conn.close()
        return result

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data where user_id = ?", (user_id,))
    return cursor.fetchone()


#### Fetch user by ID with automatic connection handling

user = get_user_by_id(user_id="35aa846f-f4f6-4d88-96ad-df660dd73af5")  # pyright: ignore

print(user)
