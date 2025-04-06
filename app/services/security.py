import re
from functools import wraps

from flask import abort, request

from app.config import settings


def validate_input(input_str: str, max_length: int = None) -> bool:
    """
    Validate user input to prevent injection attacks.

    Args:
        input_str (str): Input string to validate
        max_length (int): Maximum allowed length

    Returns:
        bool: True if input is valid
    """
    if not input_str:
        return False

    if max_length and len(input_str) > max_length:
        return False

    # Check for potentially dangerous patterns
    dangerous_patterns = [
        r"<script.*?>.*?</script>",
        r'on\w+=".*?"',
        r"javascript:",
        r"vbscript:",
        r"<\?php",
        r"<\?=",
        r"`.*?`",  # Backticks for command injection
        r"\$\{.*?\}",  # Template injection
        r"\\x[0-9a-fA-F]{2}",  # Hex encoded characters
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            return False

    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal.

    Args:
        filename (str): Original filename

    Returns:
        str: Sanitized filename
    """
    # Remove directory path components
    filename = filename.replace("../", "").replace("..\\", "")
    # Keep only whitelisted characters
    filename = re.sub(r"[^\w\-_. ]", "", filename)
    return filename.strip()


def secure_route(f):
    """
    Decorator to add security checks to routes.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check content type for JSON requests
        if request.is_json:
            try:
                data = request.get_json()
                # Validate all string fields in JSON data
                for key, value in data.items():
                    if isinstance(value, str) and not validate_input(
                        value, settings.MAX_CODE_LENGTH
                    ):
                        abort(400, description=f"Invalid input in field: {key}")
            except:
                abort(400, description="Invalid JSON data")

        # Check file uploads
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                abort(400, description="No selected file")

            # Validate file extension
            if not any(
                file.filename.lower().endswith(ext)
                for ext in settings.ALLOWED_FILE_TYPES
            ):
                abort(400, description="File type not allowed")

        return f(*args, **kwargs)

    return decorated_function
