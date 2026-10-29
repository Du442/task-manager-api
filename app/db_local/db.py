import sqlite3
import os
from dotenv import load_dotenv
from contextlib import contextmanager

# Carrega as variaveis de ambiente

load_dotenv()

# DB path

db_path = os.getenv("DB_PATH")

# Classe do Banco Local

class DBLocal():
    # Init function
    def __init__(self, file=db_path):
        self.file = file
        self.initialize_db()

    # Conexão com o db local, realizando sua ação e enfim fechando a conexão.
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

    # Cria a tabela que será utilizada na aplicação.
    def initialize_db(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name VARCHAR(255) NOT NULL,
                description TEXT,
                date DATETIME,
                is_active BOOLEAN NOT NULL,
                priority INTEGER NOT NULL
            )
""")
        print("Banco de dados iniciado.")