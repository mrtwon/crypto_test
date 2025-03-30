from src.app.exception.base import AppBaseException


class TronAddressNotFound(AppBaseException):
    status = 404
    details = 'tron address not found'
