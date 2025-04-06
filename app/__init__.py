from flask import Flask, jsonify

from app.config import settings
from app.utils.exceptions import APIError
from app.views.api import api_bp
from app.views.main import main_bp


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(settings)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Error handlers
    @app.errorhandler(APIError)
    def handle_api_error(e):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"message": "Internal server error"}), 500

    return app
