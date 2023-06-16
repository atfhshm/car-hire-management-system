from dotenv import load_dotenv
import os
import psycopg
from psycopg.rows import dict_row
import sys

__all__ = ["get_db"]


class Database:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        """
        Connect to database and return connection
        """
        print("Connecting to PostgreSQL Database...")
        try:
            load_dotenv()
            conn = psycopg.connect(
                host=os.getenv("POSTGRES_SERVER"),
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                port=os.getenv("POSTGRES_PORT"),
                row_factory=dict_row,
            )
        except psycopg.OperationalError as e:
            print(f"Could not connect to Database: {e}")
            sys.exit(1)

        return conn


def get_db():
    db = Database().connect()
    return db
