from app import create_app
from extensions import db
from models.user import User

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@local").first():
        u = User(nombre="Administrador", email="admin@local", rol="admin")
        u.set_password("admin123")
        db.session.add(u)
        db.session.commit()
        print("Admin creado: admin@local / admin123")
    else:
        print("Ya existe admin.")
