from _decimal import Decimal

from pydantic import BaseModel


class TronBalanceSchema(BaseModel):
    balance: Decimal


class SearchTronSchema(BaseModel):
    address: str
