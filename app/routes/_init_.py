# app/__init__.py
import os
from flask import Flask, jsonify
from flask_cors import CORS

from app.extensions import db, migrate, cache, limiter
from config import Config


def create_app(config_object: type[Config] = Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # CORS (optional but nice)
    CORS(app)

    # ensure instance/ exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)

    # import models so Alembic / Flask-Migrate sees them
    from app import models  # noqa: F401

    # register blueprints
    from app.routes.customers import customers_bp
    from app.routes.mechanics import mechanics_bp
    from app.routes.inventory import inventory_bp
    from app.routes.service_tickets import service_tickets_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # swagger ui (optional – assignment says adjust host later)
    try:
        from flask_swagger_ui import get_swaggerui_blueprint

        SWAGGER_URL = "/docs"
        API_URL = "/openapi.yaml"
        swaggerui_bp = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={"app_name": "Mechanic Shop API Advanced"},
        )
        app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)
    except Exception as e:
        app.logger.warning(f"Swagger UI not enabled: {e}")

    @app.get("/")
    def index():
        return jsonify(
            {
                "message": "Mechanic Shop API Advanced",
                "endpoints": [
                    "/health",
                    "/customers",
                    "/mechanics",
                    "/service-tickets",
                    "/inventory",
                    "/auth/login",
                    "/docs",
                ],
            }
        )

    @app.get("/health")
    @cache.cached(timeout=30)
    def health():
        return jsonify(
            {
                "ok": True,
                "service": "mechanic_shop_api_advanced",
                "message": "running",
            }
        )

    # local sqlite convenience
    with app.app_context():
        # only create if using sqlite
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if uri.startswith("sqlite"):
            db.create_all()

    return app
