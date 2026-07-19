from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
dashboard_bp = Blueprint("dashboard", __name__)
public_bp = Blueprint("public", __name__)

from . import auth, dashboard, public  # noqa: E402, F401
