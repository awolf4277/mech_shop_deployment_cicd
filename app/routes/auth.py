# app/routes/auth.py
import os
from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, request, jsonify, abort
from jose import jwt, JWTError

from app.models import Customer
from app.extensions import db

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("JWT_ALG", "HS256")


def create_token(customer_id: int, email: str) -> str:
    payload = {
        "sub": str(customer_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            abort(401, "missing bearer token")
        token = auth_header.split(" ", 1)[1]
        payload = decode_token(token)
        if not payload:
            abort(401, "invalid or expired token")
        # attach customer_id
        kwargs["customer_id"] = int(payload["sub"])
        return fn(*args, **kwargs)

    return wrapper


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")

    if not email:
        abort(400, "email is required")

    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        # For this assignment we DON'T create here, we just reject
        abort(401, "invalid credentials")

    token = create_token(customer.id, customer.email)
    return jsonify({"access_token": token})
