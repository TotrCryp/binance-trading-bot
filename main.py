from models import Base, db_helper
from core.domain.trading import run_trading

if __name__ == '__main__':
    Base.metadata.create_all(db_helper.engine)
    run_trading()
