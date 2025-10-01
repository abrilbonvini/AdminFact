from extensions import db
from datetime import datetime, timezone

class Factura(db.Model):
    __tablename__ = "facturas"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"))
    total = db.Column(db.Float, default=0)

    # ✅ Relación para poder usar factura.cliente en los templates
    cliente = db.relationship("Cliente", backref="facturas")

    detalles = db.relationship(
        "DetalleFactura",
        backref="factura",
        cascade="all, delete-orphan"
    )


class DetalleFactura(db.Model):
    __tablename__ = "detalle_factura"
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey("facturas.id"))
    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)