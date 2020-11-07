import psycopg2
import os

"""
Python module to simplify the integration of psycopg2
by: cooldev_
"""

def create_connection(url):
    try:
        connection = psycopg2.connect(url, sslmode='require')

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        if os.environ.get("printQuerys") == "True":
            print("printQuerys set to True")
        else:
            print("printQuerys set to False")
        if os.environ.get("printQueryResult") == "True":
            print("printQueryResult set to True")
        else:
            print("printQueryResult set to False")

    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL", error)

    return connection


# Execute and commit database querys
def execute_query(connection, query, *values):
    cursor = connection.cursor()
    try:
        try:
            cursor.execute(query, values)
            connection.commit()
        except:
            cursor.execute("rollback")
            cursor.execute(query, values)
            connection.commit()
        if os.environ.get("printQuerys") == "True":
            print(f"{query}")
    except (Exception, psycopg2.Error) as e:
        print(f"The error '{e}' occurred")


# Easily execute and fetch, ready to store in a variable
def execute_fetch_query(connection, query, *values):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        result = []
        for find in cursor.fetchall():
            result.append(dict(find))
        if os.environ.get("printQuerys") == "True":
            print(f"{query}")
        if os.environ.get("printQueryResult") == "True":
            print(f"Result: {result}")
        return result
    except (Exception, psycopg2.Error) as e:
        print(f"The error '{e}' occurred")