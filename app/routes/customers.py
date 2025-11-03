from flask import Blueprint, request, jsonify, abort
from app.extensions import db
from app.models import Customer

customers_bp = Blueprint("customers", __name__)


@customers_bp.get("/")
def list_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])


@customers_bp.post("/")
def create_customer():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        abort(400, "name and email required")
    if Customer.query.filter_by(email=email).first():
        abort(400, "email already exists")
    c = Customer(name=name, email=email)
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201
