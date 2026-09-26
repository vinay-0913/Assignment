"""
Admin User Model (for JWT authentication)
"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


class AdminUser(db.Model):
    """Admin users who can authenticate via JWT."""

    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<AdminUser {self.username}>"
