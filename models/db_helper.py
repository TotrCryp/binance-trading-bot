from core.config import DB_URL, DB_ECHO

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseHelper:
    def __init__(self, db_url: str, db_echo: bool = False):
        self.engine = create_engine(url=db_url, echo=db_echo)
        self.db_session_factory = sessionmaker(bind=self.engine,
                                               autoflush=True,
                                               autocommit=False,
                                               expire_on_commit=True)

    def get_session(self):
        return self.db_session_factory()


db_helper = DatabaseHelper(DB_URL, DB_ECHO)
