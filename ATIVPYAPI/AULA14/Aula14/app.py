import os

from flask import Flask, redirect, url_for

from controllers import api_cadastros_bp, cadastros_bp
from models import Cadastro, db

DADOS_INICIAIS = [
    {
        "nome": "Ana Silva",
        "profissao": "Engenheira de Software",
        "cep": "01310-100",
        "logradouro": "Avenida Paulista",
        "numero": "1578",
        "complemento": "Conj. 42",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "estado": "SP",
    },
    {
        "nome": "Carlos Mendes",
        "profissao": "Professor",
        "cep": "30130-010",
        "logradouro": "Avenida Afonso Pena",
        "numero": "1200",
        "complemento": "",
        "bairro": "Centro",
        "cidade": "Belo Horizonte",
        "estado": "MG",
    },
]


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "cadastros.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "aula14-cadastro-endereco-dev"

    db.init_app(app)
    app.register_blueprint(cadastros_bp)
    app.register_blueprint(api_cadastros_bp)

    with app.app_context():
        db.create_all()
        if Cadastro.query.count() == 0:
            for dados in DADOS_INICIAIS:
                db.session.add(Cadastro(**dados))
            db.session.commit()

    @app.route("/")
    def index():
        return redirect(url_for("cadastros.lista"))

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
    
