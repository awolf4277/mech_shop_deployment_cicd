from app import create_app
from app.extensions import db
from app.models import Customer, Mechanic, InventoryItem

app = create_app()
with app.app_context():
    db.create_all()

    # Seed an admin if missing
    admin = db.session.query(Customer).filter_by(email="admin@example.com").first()
    if not admin:
        admin = Customer(name="Admin", email="admin@example.com")
        admin.set_password("admin123")
        db.session.add(admin)

    # Seed sample data
    if db.session.query(Mechanic).count() == 0:
        db.session.add_all([
            Mechanic(name="Jess", specialty="Brakes", rating=4.8),
            Mechanic(name="Mo", specialty="Engines", rating=4.5),
        ])

    if db.session.query(InventoryItem).count() == 0:
        db.session.add_all([
            InventoryItem(part_name="Radiator", quantity=2, unit_price=120.0),
            InventoryItem(part_name="Brake Pads", quantity=6, unit_price=48.0),
        ])

    db.session.commit()
    print("Database initialized/seeded.")
