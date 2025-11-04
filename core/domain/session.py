from core.sender import Sender
from core.logger import get_logger
from db.trading_session import save, get, get_last_id

sender = Sender()
logger = get_logger(__name__)


class TradingSession:
    def __init__(self, force_new_session=False, start_time=0):
        self.session_id: int = 0
        if force_new_session:
            self.symbol: str = ""
            self.start_base_amount: float = 0
            self.start_quote_amount: float = 0
            self.stage: int = 0
            self.average_cost_acquired_assets: float = 0
            self.last_action: str = ""
            self.strategy_id: int = 0
            self.start_time: int = start_time
        else:
            last_id = get_last_id()
            if last_id:
                self.session_id: int = last_id
                self.get()

    def save(self):
        session_id = save(self)
        self.session_id = session_id
        logger.info("Session has been saved")

    def get(self):
        session_dict = get(self.session_id)
        if session_dict is None:
            sender.send_message(f"Trading session with id {self.session_id} not found")
            raise LookupError(f"Trading session with id {self.session_id} not found")
        self.load_from_dict(session_dict)

    def load_from_dict(self, session_dict):
        for key, value in session_dict.items():
            setattr(self, key, value)
