from flask import Flask, jsonify

from backend.config import Config
from backend.controllers import pecas_bp
from backend.database import init_database


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_database(app)
    app.register_blueprint(pecas_bp)

    @app.errorhandler(500)
    def erro_interno(_erro):
        return jsonify({"erro": "Erro interno do servidor."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
