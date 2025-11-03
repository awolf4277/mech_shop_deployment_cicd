from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import Mechanic
from ..schemas import mechanic_schema, mechanics_schema

bp = Blueprint('mechanics', __name__)

@bp.get('/')
def list_mechanics():
    rows = db.session.query(Mechanic).order_by(Mechanic.id.asc()).all()
    return jsonify({"value": mechanics_schema.dump(rows), "Count": len(rows)})

@bp.get('/top')
def top_mechanics():
    rows = db.session.query(Mechanic).order_by(Mechanic.rating.desc()).limit(5).all()
    return jsonify({"value": mechanics_schema.dump(rows), "Count": len(rows)})

@bp.post('/')
def create_mechanic():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    specialty = data.get('specialty')
    rating = float(data.get('rating', 0))
    if not name:
        return {"error": "name required"}, 400
    m = Mechanic(name=name, specialty=specialty, rating=rating)
    db.session.add(m)
    db.session.commit()
    return mechanic_schema.jsonify(m), 201
