from flask import Flask

# Internal Packages
from .config import DB_CONFIG
from sql_learning_app.app import api_bp


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.register_blueprint(api_bp)

    # DB configuration

    # Logger configuration

    return flask_app
    pass


if __name__ == "__main__":

    app = create_app()
    app.run(host="0.0.0.0", debug=False, port=5000, use_reloader=False)
