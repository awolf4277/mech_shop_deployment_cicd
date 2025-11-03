from datetime import datetime
from .extensions import db
import bcrypt

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=True)

    def set_password(self, plain: str):
        self.password_hash = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, plain: str) -> bool:
        if not self.password_hash:
            return False
        return bcrypt.checkpw(plain.encode('utf-8'), self.password_hash)

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.Float, default=0.0)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, default=0.0)

class ServiceTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    vehicle = db.Column(db.String(120), nullable=False)
    issue = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', backref=db.backref('tickets', lazy=True))
