"""
Validators — Input validation helpers.
"""
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def validate_email_format(email):
    """Return True if the email matches a valid format."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_user_data(data):
    """
    Validate required fields for user creation.

    Returns:
        str | None — Error message string, or None if valid.
    """
    required_fields = ["name", "email", "role"]
    missing = [f for f in required_fields if not data.get(f, "").strip()]

    if missing:
        return f"Missing required field(s): {', '.join(missing)}"

    if not validate_email_format(data["email"]):
        return "Invalid email format"

    return None
