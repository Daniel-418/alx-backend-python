import time
import sqlite3
import functools


query_cache = {}


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        result = func(conn, *args, **kwargs)
        conn.close()
        return result

    return wrapper


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        if kwargs["query"] in query_cache:
            return query_cache[kwargs["query"]]
        else:
            results = func(conn, *args, **kwargs)
            query_cache[kwargs["query"]] = results
            return results

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM user_data")  # pyright: ignore
print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM user_data")  # pyright: ignore
print(f"users again: {users_again}")
