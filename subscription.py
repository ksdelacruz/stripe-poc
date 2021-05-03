import json

from flask import Flask, Blueprint, request, jsonify
from config import CONFIG

import stripe
stripe.api_key = CONFIG["API_KEY"]


SUBSCRIPTION_BLUEPRINT = Blueprint("subscription_blueprint", __name__)

@SUBSCRIPTION_BLUEPRINT.route("/create-subscription", methods=["POST"])
def create_subscription():
    """
    POST DATA
        customerId (string):        obtained from /customer/add-customer
        paymentMethodId (string):   obtained from /payment/add-payment-method
        priceId (string):           obtained from front-end (ID of Pricing of a Product)
    """

    data = json.loads(request.data)
    try:
        # Attach the payment method to the customer
        stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=data['customerId'],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            data['customerId'],
            invoice_settings={
                'default_payment_method': data['paymentMethodId'],
            },
        )

        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=data['customerId'],
            items=[
                {
                    'price': data['priceId']
                }
            ],
            expand=['latest_invoice.payment_intent'],
        )
        return jsonify(subscription)
    except Exception as e:
        return jsonify(error={'message': str(e)}), 200