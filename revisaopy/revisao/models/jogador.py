from . import db
from .base import ModeloBase

class Jogador(ModeloBase):
    __tablename__ = "jogadores"

    nome = db.Column(db.String(100), nullable=False)
    posicao = db.Column(db.String(50), nullable=False)
    clube = db.Column(db.String(100), nullable=False)
    cabeceio = db.Column(db.Integer, nullable=False)
    forca = db.Column(db.Integer, nullable=False)

    @property
    def media(self):
        return (self.cabeceio + self.forca) / 2

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.posicao, cls.nome).all()
