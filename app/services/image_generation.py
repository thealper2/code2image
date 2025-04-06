import os
from io import BytesIO
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name
from pygments.style import Style
from pygments.token import Token

from app.config import ImageConfig
from app.utils.exceptions import ImageGenerationError


class CustomStyle(Style):
    """Custom syntax highlighting style"""

    styles = {
        Token.Keyword: "#FF79C6",
        Token.Keyword.Constant: "#BD93F9",
        Token.Name.Function: "#50FA7B",
        Token.Name.Class: "#8BE9FD",
        Token.String: "#F1FA8C",
        Token.Comment: "#6272A4",
        Token.Number: "#BD93F9",
    }


class ImageGenerator:
    """Enhanced image generator with more customization options"""

    def __init__(self, config: ImageConfig = None):
        self.config = config or ImageConfig()
        self.font_path = "app/static/fonts/FiraCode-Regular.ttf"

        if not os.path.exists(self.font_path):
            raise RuntimeError(f"Font file not found at: {self.font_path}")

    def generate_image(
        self,
        code: str,
        language: str,
        theme: str,
        font_size: int,
        line_numbers: bool = False,
    ) -> Tuple[BytesIO, str]:
        """
        Generate an image from code with advanced formatting options.

        Args:
            code (str): The code to render
            language (str): Programming language for syntax highlighting
            theme (str): Color theme for syntax highlighting
            font_size (int): Font size in pixels
            line_numbers (bool): Whether to show line numbers

        Returns:
            Tuple of (image_bytes, mime_type)
        """
        try:
            # Get lexer and configure formatter
            lexer = get_lexer_by_name(language)

            # Configure style based on theme
            style = self._get_style(theme)

            # Create formatter with custom options
            formatter = ImageFormatter(
                style=style,
                font_name="Fira Code",
                font_size=font_size,
                line_numbers=line_numbers,
                image_pad=10,
                line_pad=2,
                image_format="png",
            )

            # Generate highlighted image
            image_data = highlight(code, lexer, formatter)

            # Post-process the image
            pil_image = self._post_process_image(
                Image.open(BytesIO(image_data)), font_size
            )

            # Convert to bytes
            buffer = BytesIO()
            pil_image.save(buffer, format="PNG", quality=100)
            buffer.seek(0)

            return BytesIO(image_data), "image/png"

        except Exception as e:
            print(f"ERROR in generate_image: {str(e)}")
            raise ImageGenerationError(f"Image generation failed: {str(e)}")

    def _get_style(self, theme: str) -> Style:
        """Get appropriate style based on theme"""
        if theme == "custom":
            return CustomStyle

        return theme  # Pygments built-in styles

    def _post_process_image(self, image: Image.Image, font_size: int) -> Image.Image:
        """Apply additional processing to the image"""
        # Add padding
        image = ImageOps.expand(
            image, border=self.config.padding, fill=self.config.background_color
        )

        # Add watermark if enabled
        if self.config.watermark:
            image = self._add_watermark(image, font_size)

        # Add border
        image = ImageOps.expand(image, border=1, fill="#cccccc")

        return image

    def _add_watermark(self, image: Image.Image, font_size: int) -> Image.Image:
        """Add watermark text to the image"""
        try:
            draw = ImageDraw.Draw(image)
            width, height = image.size

            # Use a smaller font size for watermark
            watermark_font_size = max(font_size - 2, 8)
            font = ImageFont.truetype(self.font_path, watermark_font_size)

            watermark_text = self.config.watermark_text or "Generated with Code2Image"
            text_width = draw.textlength(watermark_text, font=font)

            # Position at bottom right with some margin
            x = width - text_width - 20
            y = height - watermark_font_size - 10

            draw.text((x, y), watermark_text, fill="#aaaaaa", font=font)
            return image
        except Exception:
            # If watermark fails, return original image
            return image

    def generate_long_code_images(
        self, code_chunks: list[str], **kwargs
    ) -> list[Tuple[BytesIO, str]]:
        """
        Generate multiple images for long code that needs to be split.

        Args:
            code_chunks (list[str]): List of code chunks to render
            kwargs (*): Arguments passed to generate_image

        Returns:
            List of (image_bytes, mime_type) tuples
        """
        return [self.generate_image(chunk, **kwargs) for chunk in code_chunks]
