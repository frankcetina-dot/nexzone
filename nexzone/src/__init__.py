from flask import Flask
from config import Config
from src.routes import auth_bp, dashboard_bp, public_bp
from src.models.database import init_database


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_class)

    # Inicializar base de datos (crea tablas e inserta datos iniciales si no existen)
    try:
        init_database()
    except Exception as e:
        print(f"[DB] Advertencia al inicializar: {e}")

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(public_bp)

    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    return app
