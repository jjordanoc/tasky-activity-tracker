import sqlite3
from sqlite3 import Error

"""
Python module to simplify the integration of sqlite3
by: cooldev_
"""
# Connect to the database
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Execute and commit database querys
def execute_query(connection, query, *values):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"{query}")
    except Error as e:
        print(f"The error '{e}' occurred")

# Easily execute and fetch, ready to store in a variable
def execute_fetch_query(connection, query, *values):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        result = []
        for find in cursor.fetchall():
            result.append(dict(find))
        print(f"{query}")
        print(f"Result: {result}")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

if __name__ == "__main__":
    db = create_connection("database.db")
    execute_fetch_query(db, "SELECT * FROM users;")