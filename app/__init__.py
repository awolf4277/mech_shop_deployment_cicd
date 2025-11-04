@'
from flask import Flask, jsonify
import os

def create_app():
    app = Flask(__name__)
    # keep CI/dev simple: use env if present, else sqlite
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @app.get("/")
    def index():
        return jsonify({
            "endpoints": ["/health", "/customers/", "/mechanics/", "/service-tickets/", "/inventory/", "/auth/login"],
            "message": "Mechanic Shop API Advanced"
        }), 200

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "service": "mechanic_shop_api_advanced", "message": "running"}), 200

    return app

# expose module-level app so "from app import app" works in tests/WSGI
app = create_app()
'@ | Set-Content -Path .\app\__init__.py -Encoding UTF8

