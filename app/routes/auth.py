from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify, current_app
from jose import jwt
from ..extensions import db
from ..models import Customer

bp = Blueprint('auth', __name__)

@bp.post('/login')
def login():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400

    user = db.session.query(Customer).filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'invalid credentials'}), 401

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=4),
        "iat": datetime.now(tz=timezone.utc),
        "scope": "user"
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
    return jsonify({"access_token": token, "token_type": "Bearer"})
