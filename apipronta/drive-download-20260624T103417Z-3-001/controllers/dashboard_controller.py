from flask import Blueprint, render_template

from models import FilmeFavorito, HistoricoBusca
from services import TmdbApi

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    api = TmdbApi()
    populares, demo = api.filmes_populares()
    melhores, _ = api.filmes_melhores()
    favoritos = FilmeFavorito.listar()
    historico = HistoricoBusca.ultimas(5)

    return render_template(
        "index.html",
        populares=populares[:6],
        melhores=melhores[:6],
        total_favoritos=len(favoritos),
        historico=historico,
        modo_demo=demo or api.usando_demo,
    )
