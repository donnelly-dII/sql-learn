from flask import Flask

# Internal Packages
from .config import DB_CONFIG, db
from sql_learning_app.app import api_bp


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.register_blueprint(api_bp)

    # DB configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG.URI
    db.init_app(app)

    # Logger configuration

    return flask_app


if __name__ == "__main__":

    app = create_app()
    app.run(host="0.0.0.0", debug=False, port=5000, use_reloader=False)
