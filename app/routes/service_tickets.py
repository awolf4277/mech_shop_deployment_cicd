# app/routes/service_tickets.py
from flask import Blueprint, request, jsonify, abort
from app.extensions import db
from app.models import ServiceTicket, Customer, Mechanic, Inventory
from app.routes.auth import token_required

service_tickets_bp = Blueprint("service_tickets", __name__)


@service_tickets_bp.get("/")
def list_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify([t.to_dict() for t in tickets])


@service_tickets_bp.post("/")
def create_ticket():
    data = request.get_json(silent=True) or {}
    description = data.get("description")
    customer_id = data.get("customer_id")

    if not description or not customer_id:
        abort(400, "description and customer_id required")

    if not Customer.query.get(customer_id):
        abort(404, "customer not found")

    ticket = ServiceTicket(description=description, customer_id=customer_id)
    db.session.add(ticket)
    db.session.commit()
    return jsonify(ticket.to_dict()), 201


@service_tickets_bp.get("/my-tickets")
@token_required
def my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return jsonify([t.to_dict() for t in tickets])


@service_tickets_bp.put("/<int:ticket_id>/edit")
def edit_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    data = request.get_json(silent=True) or {}

    # add mechanics
    add_ids = data.get("add_ids", [])
    for mid in add_ids:
        mech = Mechanic.query.get(mid)
        if mech and mech not in ticket.mechanics:
            ticket.mechanics.append(mech)

    # remove mechanics
    remove_ids = data.get("remove_ids", [])
    for mid in remove_ids:
        mech = Mechanic.query.get(mid)
        if mech and mech in ticket.mechanics:
            ticket.mechanics.remove(mech)

    # add a part (single)
    part_id = data.get("part_id")
    if part_id:
        part = Inventory.query.get(part_id)
        if part and part not in ticket.parts:
            ticket.parts.append(part)

    db.session.commit()
    return jsonify(ticket.to_dict())
