from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import ServiceTicket
from ..schemas import ticket_schema, tickets_schema

bp = Blueprint('service_tickets', __name__)

@bp.get('/')
def list_tickets():
    rows = db.session.query(ServiceTicket).order_by(ServiceTicket.id.asc()).all()
    return jsonify({"value": tickets_schema.dump(rows), "Count": len(rows)})

@bp.post('/')
def create_ticket():
    data = request.get_json(silent=True) or {}
    cid = data.get('customer_id')
    vehicle = data.get('vehicle')
    issue = data.get('issue')
    status = data.get('status', 'open')
    if not (cid and vehicle and issue):
        return {"error": "customer_id, vehicle, issue required"}, 400
    t = ServiceTicket(customer_id=cid, vehicle=vehicle, issue=issue, status=status)
    db.session.add(t)
    db.session.commit()
    return ticket_schema.jsonify(t), 201

@bp.get('/my-tickets')
def my_tickets():
    # Stub: in a real app, derive user from JWT sub
    rows = db.session.query(ServiceTicket).filter_by(customer_id=1).all()
    return jsonify({"value": tickets_schema.dump(rows), "Count": len(rows)})

@bp.put('/<int:ticket_id>/edit')
def edit_ticket(ticket_id: int):
    t = db.session.get(ServiceTicket, ticket_id)
    if not t:
        return {"error": "not found"}, 404
    data = request.get_json(silent=True) or {}
    t.status = data.get('status', t.status)
    db.session.commit()
    return ticket_schema.jsonify(t)
