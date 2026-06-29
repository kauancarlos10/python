from flask import Blueprint, render_template
from models import Jogador

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template("index.html", total_jogadores=Jogador.query.count())
