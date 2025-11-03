# app/routes/mechanics.py
from flask import Blueprint, request, jsonify, abort
from app.extensions import db
from app.models import Mechanic, ServiceTicket

mechanics_bp = Blueprint("mechanics", __name__)


@mechanics_bp.get("/")
def list_mechanics():
    mechs = Mechanic.query.all()
    return jsonify([m.to_dict() for m in mechs])


@mechanics_bp.post("/")
def create_mechanic():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    specialization = data.get("specialization")

    if not name:
        abort(400, "name is required")

    mech = Mechanic(name=name, specialization=specialization)
    db.session.add(mech)
    db.session.commit()
    return jsonify(mech.to_dict()), 201


@mechanics_bp.get("/top")
def top_mechanics():
    # mechanics ordered by number of service tickets
    # relies on service_mechanic table
    results = (
        db.session.query(Mechanic, db.func.count(ServiceTicket.id).label("tickets"))
        .join(Mechanic.service_tickets)
        .group_by(Mechanic.id)
        .order_by(db.desc("tickets"))
        .all()
    )
    return jsonify(
        [
            {
                "id": mech.id,
                "name": mech.name,
                "specialization": mech.specialization,
                "tickets": tickets,
            }
            for mech, tickets in results
        ]
    )
