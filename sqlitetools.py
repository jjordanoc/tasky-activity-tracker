import sqlite3
from sqlite3 import Error
from os import environ

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
        if environ.get("printQuerys") == "True":
            print("printQuerys set to True")
        else:
            print("printQuerys set to False")
        if environ.get("printQueryResult") == "True":
            print("printQueryResult set to True")
        else:
            print("printQueryResult set to False")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Execute and commit database querys
def execute_query(connection, query, *values):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        if environ.get("printQuerys") == "True":
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
        if environ.get("printQuerys") == "True":
            print(f"{query}")
        if environ.get("printQueryResult") == "True":
            print(f"Result: {result}")
        return result
    except Error as e:
        print(f"The error '{e}' occurred")