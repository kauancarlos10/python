from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .filme_favorito import FilmeFavorito
from .historico_busca import HistoricoBusca

__all__ = ["db", "ModeloBase", "FilmeFavorito", "HistoricoBusca"]
