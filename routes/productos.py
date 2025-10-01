from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy.exc import IntegrityError  # ✅ IMPORTANTE
from extensions import db
from models.producto import Producto

productos_bp = Blueprint("productos_bp", __name__, url_prefix="/productos")

# Listar productos
@productos_bp.route("/")
@login_required
def lista_productos():
    productos = Producto.query.all()
    return render_template("listaproducto.html", productos=productos)

# Crear producto nuevo
@productos_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    if request.method == "POST":
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        stock = request.form.get("stock")

        nuevo = Producto(
            descripcion=descripcion,
            precio=precio,
            stock=stock
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Producto agregado correctamente", "success")
        return redirect(url_for("productos_bp.lista_productos"))

    return render_template("nuevoproducto.html")

# Editar producto
@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    if request.method == "POST":
        producto.descripcion = request.form.get("descripcion")
        producto.precio = request.form.get("precio")
        producto.stock = request.form.get("stock")

        db.session.commit()
        flash("Producto actualizado correctamente", "success")
        return redirect(url_for("productos_bp.lista_productos"))

    return render_template("editarproducto.html", producto=producto)

# Eliminar producto (con control de integridad)
@productos_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)

    try:
        db.session.delete(producto)
        db.session.commit()
        flash("Producto eliminado correctamente", "success")
    except IntegrityError:
        db.session.rollback()
        flash("No se puede eliminar: el producto está asociado a una factura.", "danger")

    return redirect(url_for("productos_bp.lista_productos"))