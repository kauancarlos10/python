from flask import Blueprint, redirect, render_template, request, url_for

from models import Jogador, db

jogador_bp = Blueprint("jogador", __name__, url_prefix="/jogadores")


@jogador_bp.route("/")
def index():
    jogadores = Jogador.listar()
    return render_template("jogadores/lista.html", jogadores=jogadores)


@jogador_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        jogador = Jogador(
            nome=request.form["nome"],
            posicao=request.form["posicao"],
            clube=request.form["clube"],
            cabeceio=int(request.form["cabeceio"]),
            forca=int(request.form["forca"]),
        )
        db.session.add(jogador)
        db.session.commit()
        return redirect(url_for("jogador.index"))
    return render_template("jogadores/formulario.html")


@jogador_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    jogador = db.session.get(Jogador, id)
    if request.method == "POST":
        jogador.nome = request.form["nome"]
        jogador.posicao = request.form["posicao"]
        jogador.clube = request.form["clube"]
        jogador.cabeceio = int(request.form["cabeceio"])
        jogador.forca = int(request.form["forca"])
        db.session.commit()
        return redirect(url_for("jogador.index"))
    return render_template("jogadores/formulario.html", jogador=jogador)


@jogador_bp.route("/excluir/<int:id>")
def excluir(id):
    jogador = db.session.get(Jogador, id)
    db.session.delete(jogador)
    db.session.commit()
    return redirect(url_for("jogador.index"))
