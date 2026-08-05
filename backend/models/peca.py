from datetime import datetime
from decimal import Decimal

from backend.database import db


class Peca(db.Model):
    __tablename__ = "pecas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    codigo = db.Column(db.String(50), nullable=False, unique=True, index=True)
    fabricante = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    quantidade_minima = db.Column(db.Integer, nullable=False)
    localizacao = db.Column(db.String(100), nullable=True)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "codigo": self.codigo,
            "fabricante": self.fabricante,
            "categoria": self.categoria,
            "quantidade_estoque": self.quantidade_estoque,
            "quantidade_minima": self.quantidade_minima,
            "localizacao": self.localizacao,
            "preco_unitario": float(self.preco_unitario)
            if isinstance(self.preco_unitario, Decimal)
            else self.preco_unitario,
            "data_cadastro": self.data_cadastro.isoformat(),
        }
