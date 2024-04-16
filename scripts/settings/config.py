import os


REDIS_URL = os.getenv("REDIS_URL")
REDIS_BATCH_SIZE = 1000

DB_SETTINGS = {
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}

DATABASE_URL = os.getenv("DATABASE_URL")
