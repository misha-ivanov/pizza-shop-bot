import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()

def recreate_database() -> None:
    connection = sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH'))
    with connection:
        connection.execute("DROP TABLE IF EXISTS telegram_updates")
        connection.execute("""
            CREATE TABLE IF NOT EXISTS telegram_updates
            (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
           )
       """)
    connection.close()