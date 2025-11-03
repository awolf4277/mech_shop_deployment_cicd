# app/routes/inventory.py
from flask import Blueprint, request, jsonify, abort
from app.extensions import db, limiter
from app.models import Inventory
from app.routes.auth import token_required

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.get("/")
def list_inventory():
    items = Inventory.query.all()
    return jsonify([i.to_dict() for i in items])


@inventory_bp.post("/")
@limiter.limit("10 per minute")
@token_required
def create_inventory_item(customer_id):
    data = request.get_json(silent=True) or {}
    part_name = data.get("part_name")
    quantity = data.get("quantity", 0)
    unit_price = data.get("unit_price")

    if not part_name:
        abort(400, "part_name is required")

    item = Inventory(part_name=part_name, quantity=quantity, unit_price=unit_price)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201
