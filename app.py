from flask import Flask
from config import Config
from extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Blueprints EXISTENTES
    from routes.auth import auth_bp
    from routes.dashboard import main_bp
    from routes.clientes import clientes_bp
    from routes.productos import productos_bp
    from routes.facturas import facturas_bp

    # ✅ IMPORTANTE: Agregar este import
    from routes.reportes import reportes_bp

    # Registro de blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(reportes_bp)   # ✅ AGREGADO

    with app.app_context():
        db.create_all()
        print("Tablas creadas")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


