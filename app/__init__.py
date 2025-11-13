from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash
from datetime import timedelta
import os

# Extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'hms.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    from .models import Admin, Doctor, Patient

    @login_manager.user_loader
    def load_user(user_id):
        # user_id is in format role:id
        try:
            role, raw_id = user_id.split(":", 1)
            obj_id = int(raw_id)
        except Exception:
            return None
        if role == "admin":
            return Admin.query.get(obj_id)
        if role == "doctor":
            return Doctor.query.get(obj_id)
        if role == "patient":
            return Patient.query.get(obj_id)
        return None

    # Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.admin_routes import admin_bp
    from .routes.doctor_routes import doctor_bp
    from .routes.patient_routes import patient_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")
    app.register_blueprint(patient_bp, url_prefix="/patient")

    # Index route redirects by role
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if getattr(current_user, "role", None) == "admin":
                return ("", 302, {"Location": "/admin/dashboard"})
            if getattr(current_user, "role", None) == "doctor":
                return ("", 302, {"Location": "/doctor/dashboard"})
            if getattr(current_user, "role", None) == "patient":
                return ("", 302, {"Location": "/patient/dashboard"})
        return ("", 302, {"Location": "/login"})

    return app
