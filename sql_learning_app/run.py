from flask import Flask

# Internal Packages
from sql_learning_app.config import DB_CONFIG, db
from sql_learning_app.app import api_bp


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.register_blueprint(api_bp)

    # DB configuration
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG.URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(flask_app)

    # Logger configuration

    return flask_app


if __name__ == "__main__":

    app = create_app()
    app.run(host="0.0.0.0", debug=False, port=5000, use_reloader=False)
