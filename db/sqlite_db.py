import sqlite3
from pathlib import Path


class DbManager:
    def __init__(self, db_path):
        self._db_path = Path(db_path)
        self._conn = None

    def get_connection(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
