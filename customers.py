from flask import Flask, Blueprint
from config import CONFIG

import stripe
stripe.api_key = CONFIG["API_KEY"]


CUSTOMER_BLUEPRINT = Blueprint("customer_blueprint", __name__)

@CUSTOMER_BLUEPRINT.route("/add-customer", methods=["POST"])
def add_customer():
    response = stripe.Customer.create(
        description="My First Test Customer (created for API docs)",
    )

    return response

