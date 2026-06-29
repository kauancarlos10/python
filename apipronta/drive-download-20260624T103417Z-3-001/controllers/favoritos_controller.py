from flask import Blueprint, redirect, render_template, request, url_for

from models import FilmeFavorito

favoritos_bp = Blueprint("favoritos", __name__, url_prefix="/favoritos")


@favoritos_bp.route("/")
def listar():
    return render_template(
        "favoritos/lista.html",
        favoritos=FilmeFavorito.listar(),
    )


@favoritos_bp.route("/adicionar/<int:tmdb_id>", methods=["POST"])
def adicionar(tmdb_id):
    titulo = request.form.get("titulo", "Filme")
    poster_path = request.form.get("poster_path") or None
    nota = request.form.get("nota")
    ano = request.form.get("ano") or None

    try:
        nota = float(nota) if nota else None
    except ValueError:
        nota = None

    FilmeFavorito.adicionar(tmdb_id, titulo, poster_path, nota, ano)

    voltar = request.form.get("voltar") or url_for("favoritos.listar")
    return redirect(voltar)


@favoritos_bp.route("/remover/<int:tmdb_id>", methods=["POST"])
def remover(tmdb_id):
    FilmeFavorito.remover_por_tmdb(tmdb_id)
    voltar = request.form.get("voltar") or url_for("favoritos.listar")
    return redirect(voltar)
