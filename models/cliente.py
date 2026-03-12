from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "erp_confeccao"}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(30))
    cidade = db.Column(db.String(100))
    data_cadastro = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Cliente {self.nome}>"