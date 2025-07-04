import sqlite3
from pathlib import Path


class BaseDatabase:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def execute(self, query: str, params: tuple = ()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.fetchall()


class UserDatabase(BaseDatabase):
    def setup(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            );
        """)

    def add_user(self, name, email):
        self.execute("INSERT INTO users (name, email) VALUES (?, ?);", (name, email))

    def get_all_users(self):
        return self.execute("SELECT * FROM users;")