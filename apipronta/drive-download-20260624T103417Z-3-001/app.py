import os

from dotenv import load_dotenv
from flask import Flask

from controllers import dashboard_bp, favoritos_bp, filmes_bp
from models import db

load_dotenv()


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "streamflix.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "aula12-streamflix-dev")

    db.init_app(app)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(filmes_bp)
    app.register_blueprint(favoritos_bp)

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_globals():
        from services import TmdbApi

        return {"modo_demo": TmdbApi().usando_demo}

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
