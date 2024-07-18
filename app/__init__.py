# import config
from flask import Flask
from app.apis import bjj_fighters, bjj_matches, bjj_ranking


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@localhost:5432/bjj"
    )
    from app.models import db

    db.init_app(app)

    app.register_blueprint(bjj_fighters, url_prefix="/fighters")
    app.register_blueprint(bjj_matches, url_prefix="/matches")
    app.register_blueprint(bjj_ranking, url_prefix="/ranking")

    return app
