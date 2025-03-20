import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings

def create_database():
    """Create the database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            dbname='postgres',
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DATABASE_NAME}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {settings.DATABASE_NAME}')
            print(f"Database {settings.DATABASE_NAME} created successfully")
        else:
            print(f"Database {settings.DATABASE_NAME} already exists")
            
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
