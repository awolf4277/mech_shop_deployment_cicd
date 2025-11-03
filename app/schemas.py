from .extensions import ma
from .models import Customer, Mechanic, InventoryItem, ServiceTicket

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True
        load_instance = True
        exclude = ("password_hash",)

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

class InventoryItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryItem
        load_instance = True

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

inventory_schema = InventoryItemSchema()
inventory_list_schema = InventoryItemSchema(many=True)

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
