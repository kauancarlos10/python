from . import db
from .base import ModeloBase


class HistoricoBusca(ModeloBase):
    """Registro local das buscas feitas no site."""

    __tablename__ = "historico_buscas"

    termo = db.Column(db.String(120), nullable=False)
    resultados = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def registrar(cls, termo, resultados):
        registro = cls(termo=termo.strip(), resultados=resultados)
        db.session.add(registro)
        db.session.commit()
        return registro

    @classmethod
    def ultimas(cls, limite=8):
        return cls.query.order_by(cls.data_criacao.desc()).limit(limite).all()
