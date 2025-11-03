from flask import Blueprint, jsonify, request
from ..extensions import db, limiter
from ..models import Customer
from ..schemas import customer_schema, customers_schema

bp = Blueprint('customers', __name__)

@bp.get('/')
@limiter.limit("30/minute")
def list_customers():
    rows = db.session.query(Customer).order_by(Customer.id.asc()).all()
    return jsonify({"value": customers_schema.dump(rows), "Count": len(rows)})

@bp.post('/')
def create_customer():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email:
        return {"error": "name and email required"}, 400
    if db.session.query(Customer).filter_by(email=email).first():
        return {"error": "email already exists"}, 409

    c = Customer(name=name, email=email)
    if password:
        c.set_password(password)
    db.session.add(c)
    db.session.commit()
    return customer_schema.jsonify(c), 201
