from sqlalchemy.exc import SQLAlchemyError

from backend.database import db
from backend.models import Peca


class PecaRepository:
    """Camada exclusiva de persistência da entidade Peca."""

    def criar(self, dados):
        peca = Peca(**dados)
        try:
            db.session.add(peca)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        return peca

    def listar(self):
        return Peca.query.order_by(Peca.id).all()

    def buscar_por_id(self, peca_id):
        return db.session.get(Peca, peca_id)

    def buscar_por_codigo(self, codigo):
        return Peca.query.filter_by(codigo=codigo).first()

    def atualizar(self, peca, dados):
        for campo, valor in dados.items():
            setattr(peca, campo, valor)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        return peca

    def excluir(self, peca):
        try:
            db.session.delete(peca)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
