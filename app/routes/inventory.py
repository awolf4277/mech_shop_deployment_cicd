from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import InventoryItem
from ..schemas import inventory_schema, inventory_list_schema

bp = Blueprint('inventory', __name__)

@bp.get('/')
def list_inventory():
    rows = db.session.query(InventoryItem).order_by(InventoryItem.id.asc()).all()
    return jsonify({"value": inventory_list_schema.dump(rows), "Count": len(rows)})

@bp.post('/')
def create_inventory_item():
    data = request.get_json(silent=True) or {}
    name = data.get('part_name')
    qty = int(data.get('quantity', 0))
    price = float(data.get('unit_price', 0))
    if not name:
        return {"error": "part_name required"}, 400
    item = InventoryItem(part_name=name, quantity=qty, unit_price=price)
    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201
