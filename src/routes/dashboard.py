from flask import (
    render_template,
    session,
    redirect,
    url_for,
    flash,
    jsonify,
    request,
    g,
)
from . import dashboard_bp
from src.models.content import content_store
from src.routes.auth import token_required, generate_token, decode_token
from src.models.database import (
    get_all_users,
    add_user_db,
    update_user_db,
    delete_user_db,
    get_user_by_id,
    get_parametro,
    set_parametro,
)


@dashboard_bp.route("/")
@token_required
def dashboard():
    content_list = content_store.get_all()
    return render_template(
        "dashboard.html",
        user=session.get("user"),
        role=session.get("role"),
        content=content_list,
    )


# ---------- Contenido ----------

@dashboard_bp.route("/api/content", methods=["GET"])
def get_content():
    return jsonify(content_store.get_all())


@dashboard_bp.route("/api/content", methods=["POST"])
def add_content():
    if "user" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401
    data = request.get_json()
    added = content_store.add(data)
    return jsonify({"success": True, "item": added})


@dashboard_bp.route("/api/content/<int:content_id>", methods=["PUT"])
def update_content(content_id):
    if "user" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401
    data = request.get_json()
    updated = content_store.update(content_id, data)
    if updated:
        return jsonify({"success": True, "item": updated})
    return jsonify({"success": False, "message": "No encontrado"}), 404


@dashboard_bp.route("/api/content/<int:content_id>", methods=["DELETE"])
def delete_content(content_id):
    if "user" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401
    content_store.delete(content_id)
    return jsonify({"success": True})


@dashboard_bp.route("/api/content/<int:content_id>/play", methods=["POST"])
def increment_play(content_id):
    new_plays = content_store.increment_plays(content_id)
    return jsonify({"success": True, "plays": new_plays})


# ---------- Usuarios ----------

@dashboard_bp.route("/api/users", methods=["GET"])
def get_users():
    if "user" not in session:
        return jsonify({"success": False}), 401
    return jsonify(get_all_users())


@dashboard_bp.route("/api/users", methods=["POST"])
def add_user():
    if "user" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401
    data = request.get_json()
    if not data.get("email") or not data.get("name"):
        return jsonify({"success": False, "message": "Email y nombre requeridos"}), 400
    try:
        new_user = add_user_db(data)
        return jsonify({"success": True, "item": new_user})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@dashboard_bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if "user" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401
    data = request.get_json()
    updated = update_user_db(user_id, data)
    if updated:
        return jsonify({"success": True, "item": updated})
    return jsonify({"success": False, "message": "Usuario no encontrado"}), 404


@dashboard_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if "user" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401
    if session.get("user_id") == user_id:
        return jsonify({"success": False, "message": "No puedes eliminarte a ti mismo"}), 400
    delete_user_db(user_id)
    return jsonify({"success": True})


# ---------- Token ----------

@dashboard_bp.route("/api/refresh_token", methods=["POST"])
def refresh_token():
    if "user" not in session or "token" not in session:
        return jsonify({"success": False, "message": "No hay sesión activa"}), 401

    current_token = session.get("token")
    payload = decode_token(current_token)
    if not payload:
        return jsonify({"success": False, "message": "Token inválido"}), 401

    user = get_user_by_id(payload.get("user_id"))
    if not user:
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

    new_token = generate_token(user)
    session["token"] = new_token

    return jsonify({
        "success": True,
        "message": "Token renovado correctamente",
        "new_token": new_token,
        "expires_in_minutes": get_parametro("token_expiration_minutes", "20"),
    })


@dashboard_bp.route("/api/verify_token", methods=["GET"])
def verify_token():
    token = session.get("token")
    if not token:
        return jsonify({"valid": False, "reason": "no_token"})

    payload = decode_token(token)
    if not payload:
        session.clear()
        return jsonify({"valid": False, "reason": "expired_or_invalid"})

    return jsonify({
        "valid": True,
        "user": payload.get("name"),
        "exp": payload.get("exp"),
    })


# ---------- Parámetros ----------

@dashboard_bp.route("/api/parametros", methods=["GET"])
def get_parametros():
    if "user" not in session:
        return jsonify({"success": False}), 401
    token_min = get_parametro("token_expiration_minutes", "20")
    return jsonify({
        "success": True,
        "parametros": [
            {
                "clave": "token_expiration_minutes",
                "valor": token_min,
                "descripcion": "Duración del token JWT en minutos",
            }
        ],
    })


@dashboard_bp.route("/api/parametros", methods=["POST"])
def update_parametro():
    if "user" not in session:
        return jsonify({"success": False, "message": "No autorizado"}), 401
    data = request.get_json()
    clave = data.get("clave")
    valor = data.get("valor")
    if clave == "token_expiration_minutes":
        try:
            int(valor)
            set_parametro(clave, str(valor), "Duración del token JWT en minutos")
            return jsonify({
                "success": True,
                "message": "Parámetro actualizado. Los nuevos logins usarán este valor.",
            })
        except (TypeError, ValueError):
            return jsonify({"success": False, "message": "El valor debe ser un número entero"}), 400
    return jsonify({"success": False, "message": "Parámetro no soportado"}), 400
