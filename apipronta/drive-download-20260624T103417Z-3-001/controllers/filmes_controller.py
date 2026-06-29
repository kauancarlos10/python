from flask import Blueprint, redirect, render_template, request, url_for

from models import FilmeFavorito, HistoricoBusca
from services import TmdbApi

filmes_bp = Blueprint("filmes", __name__, url_prefix="/filmes")


@filmes_bp.route("/")
def index():
    return redirect(url_for("filmes.populares"))


@filmes_bp.route("/populares")
def populares():
    api = TmdbApi()
    filmes, demo = api.filmes_populares()
    ids_fav = {f.tmdb_id for f in FilmeFavorito.listar()}
    return render_template(
        "filmes/lista.html",
        titulo="Filmes populares",
        filmes=filmes,
        ids_favoritos=ids_fav,
        modo_demo=demo or api.usando_demo,
    )


@filmes_bp.route("/melhores")
def melhores():
    api = TmdbApi()
    filmes, demo = api.filmes_melhores()
    ids_fav = {f.tmdb_id for f in FilmeFavorito.listar()}
    return render_template(
        "filmes/lista.html",
        titulo="Melhores filmes",
        filmes=filmes,
        ids_favoritos=ids_fav,
        modo_demo=demo or api.usando_demo,
    )


@filmes_bp.route("/buscar", methods=["GET", "POST"])
def buscar():
    termo = request.args.get("q", "").strip()
    if request.method == "POST":
        termo = request.form.get("q", "").strip()

    api = TmdbApi()
    filmes = []
    demo = api.usando_demo

    if termo:
        filmes, demo = api.buscar(termo)
        HistoricoBusca.registrar(termo, len(filmes))

    ids_fav = {f.tmdb_id for f in FilmeFavorito.listar()}
    return render_template(
        "filmes/buscar.html",
        termo=termo,
        filmes=filmes,
        ids_favoritos=ids_fav,
        modo_demo=demo or api.usando_demo,
    )


@filmes_bp.route("/<int:filme_id>")
def detalhe(filme_id):
    api = TmdbApi()
    filme = api.detalhe(filme_id)
    if not filme:
        return redirect(url_for("filmes.populares"))

    streaming, demo = api.streaming(filme_id)
    favorito = FilmeFavorito.buscar_por_tmdb(filme_id)

    return render_template(
        "filmes/detalhe.html",
        filme=filme,
        streaming=streaming,
        favorito=favorito,
        modo_demo=demo or api.usando_demo,
    )
