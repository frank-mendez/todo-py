import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def create_database() -> None:
    """Create the database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        with conn.cursor() as cur:
            # Check if database exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.POSTGRES_DB,))
            if not cur.fetchone():
                # Create database if it doesn't exist
                cur.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')
                logger.info(f"Created database {settings.POSTGRES_DB}")
            else:
                logger.info(f"Database {settings.POSTGRES_DB} already exists")
                
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_database()
