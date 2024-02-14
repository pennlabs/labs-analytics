import os

REDIS_URL = "redis://localhost:6379"
REDIS_BATCH_SIZE = 1000

DB_SETTINGS = {
    "dbname": os.environ.get("DB_NAME", "judtinzhang"),
    "user": os.environ.get("DB_USER", "postgresql"),
    "password": os.environ.get("DB_PASSWORD", "postgresql"),
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
}
