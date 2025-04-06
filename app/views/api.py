import uuid
from datetime import datetime
from pathlib import Path

from flask import Blueprint, request, send_file
from werkzeug.utils import secure_filename

from app.config import ImageConfig, settings
from app.models.schemas import CodeSubmission
from app.services.code_processing import CodeProcessor
from app.services.image_generation import ImageGenerator
from app.services.security import secure_route
from app.utils.exceptions import APIError

api_bp = Blueprint("api", __name__)


@api_bp.route("/generate", methods=["POST"])
@secure_route
def generate_image():
    """API endpoint to generate code image"""
    try:
        # Handle both form data and JSON input
        if request.is_json:
            data = request.get_json()
            submission = CodeSubmission(**data)
            code = submission.code
        else:
            # Check if file was uploaded
            if "file" in request.files:
                file = request.files["file"]
                if file.filename == "":
                    raise APIError("No selected file", status_code=400)

                # Save temporarily
                upload_dir = Path(settings.UPLOAD_FOLDER)
                upload_dir.mkdir(exist_ok=True)

                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                temp_path = upload_dir / filename
                file.save(temp_path)

                # Read and validate file
                code = CodeProcessor.read_code_from_file(temp_path)

                # Clean up
                temp_path.unlink()
            else:
                # Get code from form data
                submission = CodeSubmission(
                    code=request.form.get("code", ""),
                    language=request.form.get("language", settings.DEFAULT_LANGUAGE),
                    theme=request.form.get("theme", settings.DEFAULT_THEME),
                    font_size=int(request.form.get("font_size", 14)),
                    line_numbers=bool(request.form.get("line_numbers", False)),
                    watermark_text=request.form.get("watermark_text", None),
                )
                code = submission.code

        # Generate image
        image_config = ImageConfig(
            background_color=request.form.get("background_color", "#ffffff"),
            watermark=bool(request.form.get("watermark", False)),
        )

        generator = ImageGenerator(image_config)
        image_data, mime_type = generator.generate_image(
            code=code,
            language=submission.language,
            theme=submission.theme,
            font_size=submission.font_size,
        )

        # Create response
        timestamp = datetime.utcnow().isoformat()
        image_data.seek(0)

        return send_file(
            image_data,
            mimetype=mime_type,
            as_attachment=False,  # Do not force download
            download_name=f"code_snippet_{timestamp}.png",
        )

    except Exception as e:
        raise APIError(str(e), status_code=400)


@api_bp.route("/preview", methods=["POST"])
@secure_route
def preview_image():
    """Endpoint for real-time preview (lower quality, faster generation)"""
    try:
        data = request.get_json()
        submission = CodeSubmission(**data)

        # Use faster settings for preview
        image_config = ImageConfig(padding=10, watermark=False)

        generator = ImageGenerator(image_config)
        image_data, mime_type = generator.generate_image(
            code=submission.code[:1000],  # Limit for preview
            language=submission.language,
            theme=submission.theme,
            font_size=submission.font_size,
            line_numbers=submission.line_numbers,
        )

        return send_file(image_data, mimetype=mime_type)

    except Exception as e:
        raise APIError(str(e), status_code=400)
