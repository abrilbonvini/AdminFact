from extensions import db, login_manager

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), unique=True, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)