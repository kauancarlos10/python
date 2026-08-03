from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .cadastro import Cadastro

__all__ = ["db", "ModeloBase", "Cadastro"]
