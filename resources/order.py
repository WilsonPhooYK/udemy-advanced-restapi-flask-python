from collections import Counter
from typing import Any
from flask_restful import Resource
from flask import request

from libs.strings import gettext

from stripe import error
from models.item import ItemModel
from models.order import OrderModel, ItemsInOrder
from schemas.order import OrderSchema

order_schema = OrderSchema()
multiple_order_schema = OrderSchema(many=True)

class Order(Resource):
    @classmethod
    def get(cls) -> Any:
        # return multiple_order_schema.dump(OrderModel.find_all()), 200
        return order_schema.dump(OrderModel.find_all(), many=True), 200
        
    @classmethod
    def post(cls) -> Any:
        """
        Expect a token and a list of item ids from the request body.
        Contruct an order and talk to the Stripe API to make a charge
        """
        data = request.get_json() # token + list of item ids [1, 2, 3, 5, 5, 5]
        items: list[ItemsInOrder] = []
        item_id_quantities = Counter(data["item_ids"])
        
        # Iterate over items and retrieve them from the database
        for _id, count in item_id_quantities.most_common(): # [(5, 3), (3, 1), (2, 1), (1, 1)]
            item: ItemModel = ItemModel.find_by_id(_id)
            if not item:
                return {"message": gettext("order_item_by_id_not_found").format(_id)}, 404
            
            items.append(ItemsInOrder(item_id=_id, quantity=count))
            
        order = OrderModel(items=items, status="pending")
        order.save_to_db() # this does not submit to Stripe
        
        
        try:
            order.set_status("failed")  # assume the order would fail until it's completed
            # order.charge_with_stripe(data["token"])
            order.set_status("complete")  # charge succeeded
            return order_schema.dump(order), 200
        # the following error handling is advised by Stripe, although the handling implementations are identical,
        # we choose to specify them separately just to give the students a better idea what we can expect
        except error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            return e.json_body, e.http_status
        except error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return e.json_body, e.http_status
        except error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            return e.json_body, e.http_status
        except error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return e.json_body, e.http_status
        except error.APIConnectionError as e:
            # Network communication with Stripe failed
            return e.json_body, e.http_status
        except error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return e.json_body, e.http_status
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            print(e)
            return {"message": gettext("order_error")}, 500
        