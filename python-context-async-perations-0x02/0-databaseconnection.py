import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        conn = sqlite3.connect(db_name)
        self.connection = conn

    def __enter__(self) -> sqlite3.Connection:
        return self.connection

    def __exit__(self, type, value, traceback):
        if type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()


with DatabaseConnection("users.db") as connection:
    cursor = connection.cursor()
    cursor.execute("select * from user_data")
    print(cursor.fetchall())
