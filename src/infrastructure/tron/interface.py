from _decimal import Decimal
from typing import Protocol


class ITronRepo(Protocol):
    def get_balance_by_tron_address(self, tron_address: str) -> Decimal:
        ...
