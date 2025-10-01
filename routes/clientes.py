from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models import Cliente

clientes_bp = Blueprint("clientes_bp", __name__, url_prefix="/clientes")

@clientes_bp.route("/")
@login_required
def lista_clientes():
    clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=clientes)

@clientes_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        email = request.form.get("email")

        nuevo = Cliente(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            email=email
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Cliente agregado correctamente", "success")
        return redirect(url_for("clientes_bp.lista_clientes"))

    return render_template("nuevo.html")

# ✅ Editar cliente
@clientes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":
        cliente.nombre = request.form.get("nombre")
        cliente.direccion = request.form.get("direccion")
        cliente.telefono = request.form.get("telefono")
        cliente.email = request.form.get("email")

        db.session.commit()
        flash("Cliente actualizado correctamente", "success")
        return redirect(url_for("clientes_bp.lista_clientes"))

    return render_template("editar.html", cliente=cliente)

# ✅ Eliminar cliente
@clientes_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminado correctamente", "success")
    return redirect(url_for("clientes_bp.lista_clientes"))
