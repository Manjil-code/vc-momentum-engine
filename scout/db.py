import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "data/signals.db"

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    # If cloud DB exists → use Postgres
    if database_url:
        import psycopg2
        return psycopg2.connect(database_url)

    # Otherwise fallback to local SQLite
    return sqlite3.connect(DB_PATH)
