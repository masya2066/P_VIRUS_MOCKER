import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config.init import InitConfig, set_env_from_config


def load_conn():
    db_host = str(os.getenv("DATABASE_HOST"))
    db_port = str(os.getenv("DATABASE_PORT"))
    db_name = str(os.getenv("DATABASE_NAME"))
    db_user = str(os.getenv("DATABASE_USERNAME"))
    db_password = str(os.getenv("DATABASE_PASSWORD"))

    print(f"DATABASE_HOST: {db_host}")
    print(f"DATABASE_PORT: {db_port}")
    print(f"DATABASE_NAME: {db_name}")
    print(f"DATABASE_USERNAME: {db_user}")
    print(f"DATABASE_PASSWORD: {db_password}")

    if not all([db_host, db_port, db_name, db_user, db_password]):
        raise ValueError(
            "One or more environment variables for the database connection are not set.")

    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# Initialize config and set environment variables
config = InitConfig()
set_env_from_config(config)

DATABASE_URL = load_conn()

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define the base class for declarative models
Base = declarative_base()

# Define a function to initialize the database schema


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)


# Initialize session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
