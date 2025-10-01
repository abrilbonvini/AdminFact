from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.cliente import Cliente
from models.producto import Producto
from models.factura import Factura

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def dashboard():
    clientes_count = Cliente.query.count()
    productos_count = Producto.query.count()
    facturas_count = Factura.query.count()  # ✅ total de facturas (ventas)
    
    # ✅ Por ahora mostramos las ventas igual que las facturas
    ventas_count = facturas_count

    return render_template(
        "dashboard.html",
        user=current_user,
        clientes_len=clientes_count,
        productos_len=productos_count,
        facturas_len=facturas_count,
        ventas_len=ventas_count  # ✅ esto va al template
    )

