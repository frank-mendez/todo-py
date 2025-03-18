import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

def test_connection():
    try:
        connection = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        print("Successfully connected to PostgreSQL")
        cur = connection.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        cur.close()
        connection.close()
        
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")

if __name__ == "__main__":
    test_connection()