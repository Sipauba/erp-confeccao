from flask import Blueprint, render_template, request, redirect, url_for
from models.cliente import db, Cliente

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("/clientes", methods=["GET", "POST"])
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

        return redirect(url_for("clientes.clientes"))

    lista_clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template("clientes.html", clientes=lista_clientes)


@clientes_bp.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":
        cliente.nome = request.form["nome"]
        cliente.telefone = request.form["telefone"]
        cliente.cidade = request.form["cidade"]

        db.session.commit()

        return redirect(url_for("clientes.clientes"))

    return render_template("editar_cliente.html", cliente=cliente)


@clientes_bp.route("/clientes/excluir/<int:id>")
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("clientes.clientes"))