class AppBaseException(Exception):
    status: int
    details: str