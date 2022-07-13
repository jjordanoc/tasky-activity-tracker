import psycopg2
import psycopg2.extras
from os import environ

"""
Python module to simplify the integration of psycopg2
by: cooldev_
"""

# Connect to the database with the url passed in from the main app file
def create_connection(url):
    try:
        connection = psycopg2.connect(url, sslmode='require')

        # Print PostgreSQL Connection properties
        cursor = connection.cursor()
        print (connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        # Print state of env vars
        if environ.get("printQuerys") == "True":
            print("printQuerys set to True")
        else:
            print("printQuerys set to False")
        if environ.get("printQueryResult") == "True":
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
            # Execute query and commit
            cursor.execute(query, values)
            connection.commit()
        except:
            # Rollback and try to execute query again
            cursor.execute("rollback")
            cursor.execute(query, values)
            connection.commit()
            print("Committed with rollback")
        # Print query
        if environ.get("printQuerys") == "True":
            print(f"{query}")
    except (Exception, psycopg2.Error) as e:
        print(f"The error '{e}' occurred")


# Execute and fetch data, ready to store in a variable as a list of dicts
def execute_fetch_query(connection, query, *values):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(query, values)
        result = []
        # Append finds(as dicts) into a list
        for find in cursor:
            result.append(dict(find))
        # Print query
        if environ.get("printQuerys") == "True":
            print(f"{query}")
        # Print result
        if environ.get("printQueryResult") == "True":
            print(f"Result: {result}")
        return result
    except (Exception, psycopg2.Error) as e:
        print(f"The error '{e}' occurred")