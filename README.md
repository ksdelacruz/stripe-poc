# Stripe API POC

Foobar is a Python library for dealing with word pluralization.

## Installation

1. Create a virtual environment using ```virtualenv env``` activate it via ```source env/bin/activate```.
2. Run ```pip install -r requirements.txt```.

## Running the server
1. Copy ```config_sample.py``` to ```config.py``` then supply the ```API_KEY``` and ```WEBHOOK_KEY``` (optional).
2. Run the following commands.

```bash
export FLASK_APP=run.py
flask run --port=4242
```

3. Go to ```localhost:4242/hello_world``` to confirm the server is running.

## Stripe Dashboard Configuration
1. Create a test account on Stripe.
2. Retrieve API key on ```Developers > API keys``` then ```Secret key```.
3. Go to ```Products``` and add a product of any configuration. Take note of the price ID (```API ID``` under ```Pricing```).

## Tested APIs

Check the Stripe dashboard after every call of the APIs to see what is added or changed. Use Postman (or any similar app) to do API calls.

### ```[POST] localhost:4242/customer/add-customer```
Adds a customer with bare minimum information. Returns a customer object. Take note of the customer ID.

### ```[POST] localhost:4242/payment/add-payment-method```
Adds a payment method with bare minimum information. Optional boolean field ```test_to_fail```. Returns a payment method object. Take note of the payment method ID.

### ``` [POST] localhost:4242/subscription/create-subscription```
Create a subscription. Fields are ```priceId```, ```customerId```, and ```paymentMethodId```. Returns a subscription object.

## Comments
Pretty straightforward API and documentation. The Stripe Dashboard can set everything. Once products are established on the dashboard, the API can now work. Anything else, from enrolling a customer, to adding a payment method, is easy. 