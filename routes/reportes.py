from flask import Blueprint, render_template, request
from flask_login import login_required
from models.cliente import Cliente
from models.factura import Factura
from datetime import datetime

reportes_bp = Blueprint("reportes_bp", __name__, url_prefix="/reportes")

# ✅ 0) Menú principal de reportes
@reportes_bp.route("/")
@login_required
def menu_reportes():
    return render_template("menureportes.html")

# ✅ 1) Listado de clientes para seleccionar
@reportes_bp.route("/facturas-por-cliente")
@login_required
def seleccionar_cliente():
    clientes = Cliente.query.all()
    return render_template("seleccionarcliente.html", clientes=clientes)

# ✅ 2) Facturas de un cliente puntual
@reportes_bp.route("/facturas-por-cliente/<int:cliente_id>")
@login_required
def facturas_por_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    facturas = Factura.query.filter_by(cliente_id=cliente_id).all()
    return render_template("facturasporcliente.html", cliente=cliente, facturas=facturas)

# ✅ 3) Reporte de ventas por período
@reportes_bp.route("/ventas-por-periodo", methods=["GET", "POST"])
@login_required
def ventas_por_periodo():
    facturas = []
    total_periodo = 0
    fecha_inicio = None
    fecha_fin = None

    if request.method == "POST":
        fecha_inicio_str = request.form.get("fecha_inicio")
        fecha_fin_str = request.form.get("fecha_fin")

        if fecha_inicio_str and fecha_fin_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")

            facturas = Factura.query.filter(
                Factura.fecha >= fecha_inicio,
                Factura.fecha <= fecha_fin
            ).all()

            total_periodo = sum(f.total for f in facturas)

    return render_template(
        "ventasporperiodo.html",
        facturas=facturas,
        total_periodo=total_periodo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


