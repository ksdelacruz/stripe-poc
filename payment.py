from flask import Flask, Blueprint, request
from config import CONFIG

import stripe
stripe.api_key = CONFIG["API_KEY"]


PAYMENT_BLUEPRINT = Blueprint("payment_blueprint", __name__)

@PAYMENT_BLUEPRINT.route("/add-payment-method", methods=["POST"])
def add_payment_method():
    """
    Expand this to other payment method types
    """

    data = request.get_json()
    
    cc_number = "4242424242424242"
    try:
        if data["test_to_fail"]:
            cc_number = "4000000000000002"
    except:
        pass

    response = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": cc_number,
            "exp_month": 4,
            "exp_year": 2022,
            "cvc": "314",
        },
    )

    return response