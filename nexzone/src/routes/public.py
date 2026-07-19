from flask import render_template
from . import public_bp


@public_bp.route("/public")
def public_page():
    return render_template("public_page.html")
