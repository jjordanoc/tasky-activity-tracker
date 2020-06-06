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
    result = None
    try:
        cursor.execute(query, values)
        result = cursor.fetchall()
        print(f"{query}")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")