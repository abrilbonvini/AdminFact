from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.factura import Factura, DetalleFactura
from models import Cliente, Producto

facturas_bp = Blueprint("facturas_bp", __name__, url_prefix="/facturas")


#  LISTAR FACTURAS
@facturas_bp.route("/")
@login_required
def lista_facturas():
    facturas = Factura.query.all()
    return render_template("listafactura.html", facturas=facturas)


# CREAR FACTURA
@facturas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():
    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        producto_id = request.form.get("producto_id")
        cantidad = int(request.form.get("cantidad"))
        observaciones = request.form.get("observaciones", "")

        # Crear la factura
        factura = Factura(cliente_id=cliente_id)
        db.session.add(factura)
        db.session.commit()

        # detalle
        producto = Producto.query.get(producto_id)
        precio = producto.precio

        detalle = DetalleFactura(
            factura_id=factura.id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio,
            subtotal=cantidad * precio
        )
        factura.total = detalle.subtotal

        db.session.add(detalle)
        db.session.commit()

        flash("Factura creada correctamente", "success")
        return redirect(url_for("facturas_bp.lista_facturas"))

    return render_template("nuevafactura.html", clientes=clientes, productos=productos)


#  EDITAR FACTURA
@facturas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_factura(id):
    factura = Factura.query.get_or_404(id)
    clientes = Cliente.query.all()

    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        factura.cliente_id = cliente_id
        db.session.commit()
        flash("Factura actualizada correctamente", "success")
        return redirect(url_for("facturas_bp.lista_facturas"))

    return render_template("editarfactura.html", factura=factura, clientes=clientes)


#  ELIMINAR FACTURA 
@facturas_bp.route("/eliminar/<int:id>")
@login_required
def eliminar_factura(id):
    factura = Factura.query.get_or_404(id)
    db.session.delete(factura)
    db.session.commit()
    flash("Factura eliminada correctamente", "info")
    return redirect(url_for("facturas_bp.lista_facturas"))
