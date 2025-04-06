from pathlib import Path

from app.config import settings
from app.utils.exceptions import CodeProcessingError, InvalidFileError


class CodeProcessor:
    """Handles processing and validation of code input"""

    @staticmethod
    def validate_file(file_path: Path) -> bool:
        """
        Validate the uploaded file.

        Args:
            file_path: Path to the uploaded file

        Returns:
            bool: True if file is valid

        Raises:
            InvalidFileError: If file is invalid
        """
        if not file_path.exists():
            raise InvalidFileError("File does not exist")

        if file_path.suffix.lower() not in settings.ALLOWED_FILE_TYPES:
            raise InvalidFileError(
                f"File type not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}"
            )

        if file_path.stat().st_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise InvalidFileError(
                f"File too large. Max size: {settings.MAX_FILE_SIZE_MB}MB"
            )

        return True

    @staticmethod
    def read_code_from_file(file_path: Path) -> str:
        """
        Read code from uploaded file with validation.

        Args:
            file_path: Path to the uploaded file

        Returns:
            str: The code content

        Raises:
            CodeProcessingError: If reading fails
        """
        try:
            CodeProcessor.validate_file(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            if len(code) > settings.MAX_CODE_LENGTH:
                raise CodeProcessingError(
                    f"Code too long. Max length: {settings.MAX_CODE_LENGTH} characters"
                )

            return code
        except UnicodeDecodeError:
            raise CodeProcessingError(
                "Could not decode file. Please use UTF-8 encoded files."
            )
        except Exception as e:
            raise CodeProcessingError(f"Error reading file: {str(e)}")

    @staticmethod
    def split_long_code(code: str, max_length: int = 1000) -> list[str]:
        """
        Split long code into chunks for multi-page rendering.

        Args:
            code: The code to split
            max_length: Maximum characters per chunk

        Returns:
            List of code chunks
        """
        lines = code.split("\n")
        chunks = []
        current_chunk = []
        current_length = 0

        for line in lines:
            if current_length + len(line) + 1 > max_length:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0

            current_chunk.append(line)
            current_length += len(line) + 1  # +1 for the newline character

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks
