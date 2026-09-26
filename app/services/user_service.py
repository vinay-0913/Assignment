"""
User Service — Business logic for user operations.
"""
from app import db
from app.models.user import User
from app.utils.validators import validate_user_data, validate_email_format


class UserService:
    """Encapsulates all user-related business logic."""

    @staticmethod
    def get_all_users(page=None, limit=None, search=None):
        """
        Retrieve users with optional search and pagination.

        Args:
            page:   Current page number (1-indexed).
            limit:  Number of results per page.
            search: Search term matched against name and email.

        Returns:
            dict with users list and pagination metadata.
        """
        query = User.query

        # ── Search filter ──────────────────────────────────────────
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term),
                )
            )

        # ── Pagination ─────────────────────────────────────────────
        if page and limit:
            pagination = query.order_by(User.id).paginate(
                page=page, per_page=limit, error_out=False
            )
            return {
                "users": [u.to_dict() for u in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "limit": limit,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                },
            }

        users = query.order_by(User.id).all()
        return {"users": [u.to_dict() for u in users]}

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a single user by primary key.

        Raises:
            ValueError: If user is not found.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user.to_dict()

    @staticmethod
    def create_user(data):
        """
        Create a new user after validation.

        Raises:
            ValueError: On validation failure or duplicate email.
        """
        # Validate required fields & email format
        errors = validate_user_data(data)
        if errors:
            raise ValueError(errors)

        # Check for duplicate email
        if User.query.filter_by(email=data["email"].strip().lower()).first():
            raise ValueError("A user with this email already exists")

        user = User(
            name=data["name"].strip(),
            email=data["email"].strip().lower(),
            role=data["role"].strip(),
        )
        db.session.add(user)
        db.session.commit()

        return user.to_dict()

    @staticmethod
    def update_user(user_id, data):
        """
        Update an existing user.

        Raises:
            ValueError: If user not found, validation fails, or duplicate email.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        # If email is being changed, validate format & uniqueness
        if "email" in data:
            if not validate_email_format(data["email"]):
                raise ValueError("Invalid email format")
            existing = User.query.filter(
                User.email == data["email"].strip().lower(),
                User.id != user_id,
            ).first()
            if existing:
                raise ValueError("A user with this email already exists")
            user.email = data["email"].strip().lower()

        if "name" in data:
            user.name = data["name"].strip()
        if "role" in data:
            user.role = data["role"].strip()

        db.session.commit()
        return user.to_dict()

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user by ID.

        Raises:
            ValueError: If user is not found.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        db.session.delete(user)
        db.session.commit()
        return True
