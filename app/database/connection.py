import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

READONLY_DB_USER = os.getenv("READONLY_DB_USER")
READONLY_DB_PASSWORD = os.getenv("READONLY_DB_PASSWORD")

# Validate configuration
if not all([DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Missing database configuration.")

if not all([DB_USER, DB_PASSWORD]):
    raise ValueError("Admin database credentials are missing.")

if not all([READONLY_DB_USER, READONLY_DB_PASSWORD]):
    raise ValueError("Read-only database credentials are missing.")


# Common database URL configuration
def create_database_url(username, password):
    return URL.create(
        drivername="postgresql+psycopg",
        username=username,
        password=password,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
        query={"sslmode": "require"},
    )


# Admin database engine
DATABASE_URL = create_database_url(DB_USER, DB_PASSWORD)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=3,
    max_overflow=2,
    pool_recycle=1800,
)


# Read-only database engine
READONLY_DATABASE_URL = create_database_url(
    READONLY_DB_USER,
    READONLY_DB_PASSWORD,
)

readonly_engine = create_engine(
    READONLY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=3,
    max_overflow=0,
    pool_recycle=1800,
    connect_args={"options": "-c default_transaction_read_only=on"},
)


# Test admin database connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Admin database connection successful!")
            print("Test result:", result.scalar())

    except SQLAlchemyError as error:
        print("Admin database connection failed!")
        print(error)


# Test read-only database connection
def test_readonly_connection():
    try:
        with readonly_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Read-only database connection successful!")
            print("Test result:", result.scalar())

    except SQLAlchemyError as error:
        print("Read-only database connection failed!")
        print(error)


if __name__ == "__main__":
    test_connection()
    test_readonly_connection()
