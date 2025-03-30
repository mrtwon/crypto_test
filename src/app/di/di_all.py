from fastapi import FastAPI
from .di_setup import di_setup
from .di_tron import di_tron
from .di_stat import di_stat


def di_all(app: FastAPI):
    di_setup(app)
    di_tron(app)
    di_stat(app)
