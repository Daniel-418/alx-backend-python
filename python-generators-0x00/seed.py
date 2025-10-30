import uuid
import mysql.connector


def connect_db():
    connection = 0
    try:
        connection = mysql.connector.connect(
            user="daniel", password="daniel", host="127.0.0.1"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"error creating connection: {e}")
        return None


def create_database(connection: mysql.connector.MySQLConnection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS ALX_prodev;
        """)
        connection.commit()
    except mysql.connector.Error as e:
        print(f"error creating database: {e}")


def connect_to_prodev():
    connection = 0
    try:
        connection = mysql.connector.connect(
            user="daniel", password="daniel", host="127.0.0.1", database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"error creating connection: {e}")


def create_table(connection: mysql.connector.MySQLConnection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data(
                user_id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
                name VARCHAR(150) NOT NULL,
                email VARCHAR(100) NOT NULL,
                age INT NOT NULL
            );
        """)
        connection.commit()
    except mysql.connector.Error as e:
        print(f"error creating table: {e}")


def insert_data(connection: mysql.connector.MySQLConnection, data):
    cursor = connection.cursor()
    try:
        with open(data, "r", encoding="utf-8") as f:
            for line in f:
                if not line:
                    continue
                line_items = [x.strip().strip('"') for x in line.strip().split(",")]
                if len(line_items) != 3:
                    continue
                if (
                    line_items[0].lower() == "name"
                    and line_items[1].lower() == "email"
                    and line_items[2].lower() == "age"
                ):
                    continue
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (str(uuid.uuid4()), line_items[0], line_items[1], line_items[2]),
                )
        connection.commit()
    except mysql.connector.Error as e:
        print(f"database error: {e}")
    except FileNotFoundError as e:
        print(f"file not found: {e}")
    except Exception as e:
        print(f"error: {e}")
