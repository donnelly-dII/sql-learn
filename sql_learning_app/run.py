from flask import Flask


def create_app() -> Flask:
    flask_app = Flask(__name__)

    # DB configuration

    # Logger configuration

    return flask_app
    pass


if __name__ == "__main__":

    app = create_app()
    app.run(host="0.0.0.0", debug=False, port=5000, use_reloader=False)
