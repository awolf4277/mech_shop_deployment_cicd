from datetime import datetime
from app.extensions import db

service_mechanic = db.Table(
    "service_mechanic",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanics.id"), primary_key=True),
)

service_part = db.Table(
    "service_part",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("inventory_id", db.Integer, db.ForeignKey("inventory.id"), primary_key=True),
)


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    service_tickets = db.relationship("ServiceTicket", backref="customer", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120))

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_mechanic,
        back_populates="mechanics",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
        }


class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_part,
        back_populates="parts",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "part_name": self.part_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
        }


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    status = db.Column(db.String(50), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    mechanics = db.relationship(
        "Mechanic",
        secondary=service_mechanic,
        back_populates="service_tickets",
    )

    parts = db.relationship(
        "Inventory",
        secondary=service_part,
        back_populates="service_tickets",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "customer_id": self.customer_id,
            "mechanics": [m.id for m in self.mechanics],
            "parts": [p.id for p in self.parts],
        }
