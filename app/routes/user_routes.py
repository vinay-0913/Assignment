"""
User Routes — REST API endpoints for user management.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.user_service import UserService

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    GET /users
    Query params:
        - search : filter by name or email
        - page   : page number (1-indexed)
        - limit  : results per page
    """
    search = request.args.get("search", None)
    page = request.args.get("page", None, type=int)
    limit = request.args.get("limit", 10, type=int)

    result = UserService.get_all_users(page=page, limit=limit, search=search)

    return jsonify({"success": True, "data": result}), 200


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """GET /users/<id> — Retrieve a single user by ID."""
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify({"success": True, "data": user}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@user_bp.route("/users", methods=["POST"])
def create_user():
    """POST /users — Create a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Request body must be JSON"}), 400

    try:
        user = UserService.create_user(data)
        return jsonify({"success": True, "data": user}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    """PUT /users/<id> — Update an existing user (JWT protected)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Request body must be JSON"}), 400

    try:
        user = UserService.update_user(user_id, data)
        return jsonify({"success": True, "data": user}), 200
    except ValueError as e:
        error_msg = str(e)
        status = 404 if error_msg == "User not found" else 400
        return jsonify({"success": False, "error": error_msg}), status


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """DELETE /users/<id> — Delete a user (JWT protected)."""
    try:
        UserService.delete_user(user_id)
        return jsonify({"success": True, "message": "User deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
