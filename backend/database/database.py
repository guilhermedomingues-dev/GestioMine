from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_database(app):
    """Vincula o SQLAlchemy à aplicação e cria as tabelas mapeadas."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
