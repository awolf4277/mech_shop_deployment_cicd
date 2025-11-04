# flask_app.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    # For local debugging only; use 'flask run' normally
    app.run(host="127.0.0.1", port=5000, debug=True)
