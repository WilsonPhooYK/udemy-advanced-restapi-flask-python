import os
import stripe
from dataclasses import dataclass

from db import db
from models.item import ItemModel

Model = db.Model

CURRENCY = "usd"

# items_to_orders = db.Table(
#     "items_to_orders",
#     db.Column("item_id", db.Integer, db.ForeignKey("items.id")),
#     db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
# )

# [1, 3]
# [2, 3]
# [3, 5]

@dataclass
class ItemsInOrder(Model):
    __tablename__ = "items_to_orders"
    
    id: int = db.Column(db.Integer, primary_key=True)
    item_id: int = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id: int = db.Column(db.Integer, db.ForeignKey("orders.id"))
    quantity: int = db.Column(db.Integer)
    
    item:ItemModel = db.relationship("ItemModel")
    order:"OrderModel" = db.relationship("OrderModel", back_populates="items") 

@dataclass
class OrderModel(Model):
    """
    Constructor: Sets status amd items. When items.ItemsInOrder is set as items is pass in,
    item_id and quantity is set, but as we back_populates the order, ItemsInOrder.order_id is
    set according to the OrderModel.id.
    
    back_populates="items" in ItemsInOrder will update the order in ItemsInOrder
    """
    __tablename__ = "orders"
    
    id: int = db.Column(db.Integer, primary_key=True)
    status: str = db.Column(db.String(20), nullable=False)
    
    # back_populates: make sure the order in ItemsInOrder updates when we update items
    items: list[ItemsInOrder] = db.relationship("ItemsInOrder", back_populates="order", lazy="dynamic")
    
    @property
    def description(self):
        """
        Generates a simple string representing this order, in the format of "5x chair, 2x table"
        """
        item_counts = [f"{i.quantity}x {i.item.name}" for i in self.items]
        return ",".join(item_counts)
    
    @property
    def amount(self):
        return int(sum([item_data.item.price * item_data.quantity for item_data in self.items]) * 100)
    
    @property
    def quantity(self):
        return int(sum([item_data.quantity for item_data in self.items]))
    
    @classmethod
    def find_all(cls) -> list["OrderModel"]:
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()
    
    def charge_with_stripe(self, token: str) -> stripe.PaymentIntent:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        
        # return stripe.Charge.create( # type: ignore
        #     amount=self.amount, # amount of cents (100 means USD $1.00)
        #     currency=CURRENCY,
        #     description=self.description,
        #     source=token
        # )
        intent = stripe.PaymentIntent.create(
            amount=self.amount,
            currency=CURRENCY
        )
        
        # session = stripe.checkout.Session.create(
        #     payment_method_types=['card'],
        #     line_items=[{
        #         'price_data': {
        #         'product': self.description,
        #         'unit_amount': self.amount,
        #         'currency': CURRENCY,
        #         },
        #         'quantity': self.quantity,
        #     }],
        #     mode='payment',
        #     success_url='https://example.com/success',
        #     cancel_url='https://example.com/cancel',
        # )
        
        print(intent)
        return intent
    
    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.save_to_db()
        
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()