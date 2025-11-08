import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        result = func(conn, *args, **kwargs)
        conn.close()
        return result

    return wrapper


def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            results = func(conn, *args, **kwargs)
            conn.commit()
            print("Success!")
            return results
        except sqlite3.Error as e:
            print(f"Error: {e}")
            print("Rolling back...")
            conn.rollback()

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, old_email, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_data SET email = ? WHERE email = ?", (new_email, old_email)
    )


#### Update user's email with automatic transaction handling

update_user_email(
    old_email="Ross.Reynolds21@hotmail.com", new_email="Crawford_Cartwright@hotmail.com"
)  # pyright: ignore
