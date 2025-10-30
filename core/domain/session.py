from core.sender import Sender
from core.logger import get_logger
from db.trading_session import save, get

sender = Sender()
logger = get_logger(__name__)


class TradingSession:
    def __init__(self, session_id=0):
        self.session_id: int = session_id
        self.symbol: str = ""
        self.start_base_amount: float = 0
        self.start_quote_amount: float = 0
        self.stage: int = 0
        self.average_cost_acquired_assets: float = 0
        self.last_action: str = ""
        self.strategy_id: int = 0
        if self.session_id > 0:
            self.get()

    def save(self):
        session_id = save(self)
        self.session_id = session_id
        logger.info("Strategy has been saved")

    def get(self):
        session_dict = get(self.session_id)
        if session_dict is None:
            sender.send_message(f"Trading session with id {self.session_id} not found")
            raise LookupError(f"Trading session with id {self.session_id} not found")
        self.load_from_dict(session_dict)

    def load_from_dict(self, session_dict):
        for key, value in session_dict.items():
            setattr(self, key, value)


