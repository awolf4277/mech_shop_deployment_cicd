from flask import Flask, jsonify
import os

def create_app():
    app = Flask(__name__)
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

# Expose module-level app so tests/WSGI can `from app import app`
app = create_app()
"@
[System.IO.File]::WriteAllText("$PWD\app\__init__.py", $py, [System.Text.UTF8Encoding]::new($false))