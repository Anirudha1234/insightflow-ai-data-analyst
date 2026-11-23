import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

# Read database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Validate configuration
if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("Missing database environment variables.")

# Construct database URL safely
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800,
)


# Test database connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print("Test result:", result.scalar())

    except SQLAlchemyError as error:
        print("Database connection failed!")
        print(error)


if __name__ == "__main__":
    test_connection()


# Read-only connection (used by AI agent)
READONLY_DB_USER = os.getenv("READONLY_DB_USER")
READONLY_DB_PASSWORD = os.getenv("READONLY_DB_PASSWORD")

if not all([READONLY_DB_USER, READONLY_DB_PASSWORD]):
    raise ValueError("Read-only database credentials are missing.")

READONLY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=READONLY_DB_USER,
    password=READONLY_DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

readonly_engine = create_engine(
    READONLY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=0,
    connect_args={
        "options": "-c default_transaction_read_only=on -c statement_timeout=10000"
    },
)
