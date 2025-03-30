from _decimal import Decimal
from tronpy import Tron

from src.infrastructure.tron.interface import ITronRepo


class TronRepo(ITronRepo):
    def __init__(self):
        self.tron_client = Tron()

    def get_balance_by_tron_address(self, tron_address: str) -> Decimal:
        return self.tron_client.get_account_balance(tron_address)
