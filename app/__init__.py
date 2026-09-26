"""
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────────
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/users"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-change-me")
    app.config["PER_PAGE_DEFAULT"] = 10

    # ── Extensions ─────────────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # ── Register Blueprints ────────────────────────────────────────
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    # ── Create tables ──────────────────────────────────────────────
    with app.app_context():
        from app.models.user import User          # noqa: F401
        from app.models.admin import AdminUser    # noqa: F401
        db.create_all()

    # ── Global error handlers ──────────────────────────────────────
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app
