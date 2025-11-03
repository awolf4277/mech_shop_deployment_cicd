import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from .extensions import db, ma, limiter, cache
from flask_cors import CORS

def create_app():
    # Load .env early
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Base config, then instance/config.py (if exists)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///mech_shop.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-change-me"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me"),
        RATELIMIT_DEFAULT=os.getenv("RATELIMIT_DEFAULT", "100/hour"),
        CACHE_TYPE=os.getenv("CACHE_TYPE", "SimpleCache"),
        CACHE_DEFAULT_TIMEOUT=int(os.getenv("CACHE_DEFAULT_TIMEOUT", "120")),
    )
    app.config.from_pyfile("config.py", silent=True)

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    # Rate limiter
    limiter.init_app(app)

    # Register blueprints
    from .routes.customers import bp as customers_bp
    from .routes.mechanics import bp as mechanics_bp
    from .routes.inventory import bp as inventory_bp
    from .routes.service_tickets import bp as tickets_bp
    from .routes.auth import bp as auth_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.get("/")
    def index():
        return jsonify({
            "endpoints": [
                "/health",
                "/customers/",
                "/mechanics/",
                "/mechanics/top",
                "/service-tickets/",
                "/inventory/",
                "/auth/login",
                "/docs"
            ],
            "message": "Mechanic Shop API Advanced"
        })

    @app.get("/health")
    @cache.cached(timeout=30)
    def health():
        return jsonify({"ok": True, "service": "mechanic_shop_api_advanced", "message": "running"})

    # Optional docs redirect (if you wire Swagger later)
    @app.get("/docs")
    def docs():
        return jsonify({"info": "Swagger UI not installed. Install flask-swagger-ui or use Postman."}), 200

    return app
