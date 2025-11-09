import sqlite3


class ExecuteQuery:
    def __init__(self, db_name: str, query: str, parameter: tuple = ()):
        conn = sqlite3.connect(db_name)
        self.connection = conn
        self.query = query
        self.parameter = parameter

    def __enter__(self):
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.parameter)
        result = cursor.fetchall()
        cursor.close()
        return result

    def __exit__(self, type, value, traceback):
        if type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()


with ExecuteQuery("users.db", "select * from user_data where age > ?", (25,)) as result:
    print(result)
