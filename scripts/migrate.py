import psycopg2
from settings.config import DB_SETTINGS

def instantiate():
    CREATE_COMMAND = """
    CREATE TABLE Event (
        id SERIAL PRIMARY KEY,
        pennkey VARCHAR(50),
        timestamp TIMESTAMP,
        event VARCHAR(256),
        data VARCHAR(256)
    );
    """

    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute(CREATE_COMMAND)
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")
 
if __name__ == "__main__":
    instantiate()

# brew services start postgresql