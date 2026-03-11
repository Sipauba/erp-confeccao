import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        cidade = request.form["cidade"]

        novo_cliente = Cliente(
            nome=nome,
            telefone=telefone,
            cidade=cidade
        )

        db.session.add(novo_cliente)
        db.session.commit()

        return redirect(url_for("clientes"))

    lista_clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template("clientes.html", clientes=lista_clientes)


@app.route("/clientes/excluir/<int:id>")
def excluir_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("clientes"))


@app.route("/clientes/editar/<int:id>", methods=["GET","POST"])
def editar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":

        cliente.nome = request.form["nome"]
        cliente.telefone = request.form["telefone"]
        cliente.cidade = request.form["cidade"]

        db.session.commit()

        return redirect(url_for("clientes"))

    return render_template("editar_cliente.html", cliente=cliente)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
