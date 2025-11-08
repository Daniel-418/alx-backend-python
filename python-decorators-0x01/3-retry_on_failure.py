import time
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


def retry_on_failure(retries, delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            for i in range(retries):
                try:
                    results = func(conn, *args, **kwargs)
                    return results
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
                    print("retrying...")
                    time.sleep(delay)
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    print("retrying...")
                    time.sleep(delay)
                    continue

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=12, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()  # pyright: ignore
print(users)
