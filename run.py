import os
import json

from flask import Flask, jsonify, request
import stripe

from config import CONFIG
from customers import CUSTOMER_BLUEPRINT
from payment import PAYMENT_BLUEPRINT
from subscription import SUBSCRIPTION_BLUEPRINT

app = Flask(__name__)

app.register_blueprint(CUSTOMER_BLUEPRINT, url_prefix='/customer')
app.register_blueprint(PAYMENT_BLUEPRINT, url_prefix='/payment')
app.register_blueprint(SUBSCRIPTION_BLUEPRINT, url_prefix='/subscription')


# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = CONFIG["API_KEY"]


@app.route("/hello_world")
def hello_world():
    return "Hello world!"


@app.route('/stripe-webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    webhook_secret = CONFIG["WEBHOOK_SECRET_KEY"]
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        print(data)

    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        print(data)

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print(data)

    return jsonify({'status': 'success'})