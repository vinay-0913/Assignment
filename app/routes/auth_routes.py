"""
Auth Routes — JWT registration and login endpoints.
"""
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """POST /auth/register — Register a new admin user."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Request body must be JSON"}), 400

    try:
        result = AuthService.register(
            username=data.get("username"),
            password=data.get("password"),
        )
        return jsonify({"success": True, "data": result}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """POST /auth/login — Authenticate and receive a JWT token."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Request body must be JSON"}), 400

    try:
        result = AuthService.login(
            username=data.get("username"),
            password=data.get("password"),
        )
        return jsonify({"success": True, "data": result}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 401
