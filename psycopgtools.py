import psycopg2
import os

"""
Python module to simplify the integration of sqlite3
by: cooldev_
"""



try:
    DATABASE_URL = os.environ['DATABASE_URL']

    connection = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

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