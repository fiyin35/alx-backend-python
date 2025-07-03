from mysql.connector import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def stream_users():
    """a generator that fetches rows one by one from user_data table"""

    connection = connect(
        host = getenv("HOST"),
        user = getenv("DBUSER", "root"),
        password = getenv("PASSWORD"),
        database = getenv("DBNAME", "ALX_prodev")
    )

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()