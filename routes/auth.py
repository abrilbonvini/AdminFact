from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models.user import User
from extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.dashboard"))

        flash("Credenciales inválidas", "danger")

    # Formulario original, sigue funcionando para render
    from forms.auth import LoginForm
    form = LoginForm()
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")
        rol = request.form.get("rol", "user")

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios", "warning")
            return redirect(url_for("auth.register"))

        # Verificar que el email no esté en uso
        if User.query.filter_by(email=email).first():
            flash("El email ya está registrado", "danger")
            return redirect(url_for("auth.register"))

        nuevo_user = User(
            nombre=nombre,
            email=email,
            rol=rol
        )
        nuevo_user.set_password(password)

        try:
            db.session.add(nuevo_user)
            db.session.commit()
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {str(e)}", "danger")

    # Renderiza un formulario HTML simple
    return render_template("register.html")