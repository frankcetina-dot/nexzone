import jwt
import datetime
from functools import wraps
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
    g,
)
from . import auth_bp
from src.models.database import validate_user, get_parametro


def get_token_expiration_minutes():
    try:
        val = get_parametro("token_expiration_minutes", "20")
        return int(val)
    except (TypeError, ValueError):
        return 20


def generate_token(user):
    minutes = get_token_expiration_minutes()
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes),
    }
    secret = current_app.config["JWT_SECRET"]
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token):
    try:
        secret = current_app.config["JWT_SECRET"]
        return jwt.decode(token, secret, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = validate_user(email, password)

        if user:
            token = generate_token(user)
            session["user"] = user["name"]
            session["role"] = user["role"]
            session["token"] = token
            session["user_id"] = user["id"]
            flash("Sesión iniciada correctamente.", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Credenciales incorrectas. Verifica tu correo y contraseña.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("auth.login"))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token")
        if not token:
            flash("Debes iniciar sesión.", "error")
            return redirect(url_for("auth.login"))

        payload = decode_token(token)
        if not payload:
            session.clear()
            flash("Tu sesión ha expirado. Inicia sesión nuevamente.", "error")
            return redirect(url_for("auth.login"))

        g.current_user = payload
        return f(*args, **kwargs)

    return decorated
