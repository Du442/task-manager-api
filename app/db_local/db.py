import sqlite3
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

db_path = os.getenv("DB_PATH")

class DBLocal():
    def __init__(self, file=db_path):
        self.file = file
        self.initialize_db()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.file)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def initialize_db(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name VARCHAR(255) NOT NULL,
                description TEXT,
                date DATETIME,
                is_active BOOLEAN NOT NULL
            )
""")
        print("Banco de dados iniciado.")