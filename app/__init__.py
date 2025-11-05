from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "service": "mechanic_shop_api_advanced", "message": "running"}), 200

    return app

app = create_app()

