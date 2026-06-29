from . import db
from .base import ModeloBase


class FilmeFavorito(ModeloBase):
    """Filmes salvos pelo usuário (dados espelhados da API TMDB)."""

    __tablename__ = "filmes_favoritos"

    tmdb_id = db.Column(db.Integer, nullable=False, unique=True)
    titulo = db.Column(db.String(200), nullable=False)
    poster_path = db.Column(db.String(255), nullable=True)
    nota = db.Column(db.Float, nullable=True)
    ano = db.Column(db.String(10), nullable=True)

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()

    @classmethod
    def buscar_por_tmdb(cls, tmdb_id):
        return cls.query.filter_by(tmdb_id=tmdb_id).first()

    @classmethod
    def adicionar(cls, tmdb_id, titulo, poster_path=None, nota=None, ano=None):
        if cls.buscar_por_tmdb(tmdb_id):
            return None
        fav = cls(
            tmdb_id=tmdb_id,
            titulo=titulo,
            poster_path=poster_path,
            nota=nota,
            ano=ano,
        )
        db.session.add(fav)
        db.session.commit()
        return fav

    @classmethod
    def remover_por_tmdb(cls, tmdb_id):
        fav = cls.buscar_por_tmdb(tmdb_id)
        if fav:
            db.session.delete(fav)
            db.session.commit()
            return True
        return False
