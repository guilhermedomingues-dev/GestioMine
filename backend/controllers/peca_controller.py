from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from backend.services import PecaService, ValidacaoPecaError

pecas_bp = Blueprint("pecas", __name__)
service = PecaService()


def _dados_json():
    if not request.is_json:
        raise ValidacaoPecaError(
            "O Content-Type deve ser application/json."
        )

    return request.get_json(silent=True)


@pecas_bp.post("/pecas")
def criar_peca():
    try:
        peca = service.criar(_dados_json())
        return jsonify(peca.to_dict()), 201
    except ValidacaoPecaError as erro:
        return jsonify({"erro": str(erro)}), 400
    except SQLAlchemyError:
        return jsonify({"erro": "Erro interno ao salvar a peça."}), 500


@pecas_bp.get("/pecas")
def listar_pecas():
    try:
        return jsonify([peca.to_dict() for peca in service.listar()]), 200
    except SQLAlchemyError:
        return jsonify({"erro": "Erro interno ao listar as peças."}), 500


@pecas_bp.get("/pecas/<int:peca_id>")
def buscar_peca(peca_id):
    try:
        peca = service.buscar_por_id(peca_id)

        if not peca:
            return jsonify({"erro": "Peça não encontrada."}), 404

        return jsonify(peca.to_dict()), 200
    except SQLAlchemyError:
        return jsonify({"erro": "Erro interno ao buscar a peça."}), 500


@pecas_bp.put("/pecas/<int:peca_id>")
def atualizar_peca(peca_id):
    try:
        peca = service.atualizar(peca_id, _dados_json())

        if not peca:
            return jsonify({"erro": "Peça não encontrada."}), 404

        return jsonify(peca.to_dict()), 200
    except ValidacaoPecaError as erro:
        return jsonify({"erro": str(erro)}), 400
    except SQLAlchemyError:
        return jsonify({"erro": "Erro interno ao atualizar a peça."}), 500


@pecas_bp.delete("/pecas/<int:peca_id>")
def excluir_peca(peca_id):
    try:
        if not service.excluir(peca_id):
            return jsonify({"erro": "Peça não encontrada."}), 404

        return "", 204
    except SQLAlchemyError:
        return jsonify({"erro": "Erro interno ao excluir a peça."}), 500
