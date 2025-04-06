from typing import Optional

from werkzeug.exceptions import HTTPException


class APIError(HTTPException):
    """Base API exception class"""

    def __init__(
        self, message: str, status_code: int = 400, payload: Optional[dict] = None
    ):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self):
        """Convert exception to dictionary for JSON response"""
        rv = dict(self.payload or ())
        rv["message"] = self.message
        rv["status_code"] = self.status_code
        return rv


class ImageGenerationError(APIError):
    """Exception raised when image generation fails"""

    def __init__(self, message: str):
        super().__init__(message, 500)


class InvalidFileError(APIError):
    """Exception raised for invalid file uploads"""

    def __init__(self, message: str):
        super().__init__(message, 400)


class CodeProcessingError(APIError):
    """Exception raised during code processing"""

    def __init__(self, message: str):
        super().__init__(message, 400)
