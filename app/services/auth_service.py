"""
Auth Service — Business logic for JWT authentication.
"""
from app import db
from app.models.admin import AdminUser
from flask_jwt_extended import create_access_token


class AuthService:
    """Handles admin registration and login."""

    @staticmethod
    def register(username, password):
        """
        Register a new admin user.

        Raises:
            ValueError: If username already exists or fields are missing.
        """
        if not username or not password:
            raise ValueError("Username and password are required")

        if AdminUser.query.filter_by(username=username).first():
            raise ValueError("Username already exists")

        admin = AdminUser(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        return {"message": "Admin user registered successfully"}

    @staticmethod
    def login(username, password):
        """
        Authenticate and return a JWT access token.

        Raises:
            ValueError: On invalid credentials.
        """
        if not username or not password:
            raise ValueError("Username and password are required")

        admin = AdminUser.query.filter_by(username=username).first()
        if not admin or not admin.check_password(password):
            raise ValueError("Invalid username or password")

        access_token = create_access_token(identity=str(admin.id))
        return {"access_token": access_token}
