from flask import Flask, render_template, request, jsonify
import stripe
import json
import os

app = Flask(__name__)
# This is your test secret API key.
stripe.api_key = 'sk_test_your_key'

# Replace this endpoint secret with your endpoint's unique secret
# If you are testing with the CLI, find the secret by running 'stripe listen'
# If you are using an endpoint defined with the API or dashboard, look in your webhook settings
# at https://dashboard.stripe.com/webhooks
endpoint_secret = 'whsec_your_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tnc')
def tnc():
    return render_template('tnc.html')

@app.route('/onboard', methods=['POST'])
def onboard():

    account = stripe.Account.create(type="express")
    
    # return_url = when user completes onboarding
    # refresh_url = need onboard again
    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url="https://cashshope.japaneast.cloudapp.azure.com",
        return_url="https://cashshope.japaneast.cloudapp.azure.com/return",
        type="account_onboarding",
    )

    return jsonify(url=account_link,
            account_id=account.id)
 
@app.route('/reauth', methods=['POST'])
def reauth():
    content = request.json

    account = stripe.Account.retrieve(content["account_id"])

    try:
        account_link = stripe.AccountLink.create(
                account=account.id,
                refresh_url="https://cashshope.japaneast.cloudapp.azure.com",
                return_url="https://cashshope.japaneast.cloudapp.azure.com/return",
                type="account_onboarding",
                )
        return jsonify(url=account_link,
                account_id=account.id)
    except:
        jsonify(success=False)

@app.route('/account', methods=['POST'])
def account():
    content = request.json
    account_details = stripe.Account.retrieve(content['account_id'])
    return jsonify(account_details)

@app.route('/dashboard', methods=['POST'])
def dashboard():
    content = request.json

    dashboard_url = stripe.Account.create_login_link(content['account_id'])

    return jsonify(dashboard_url)

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    content = request.json

    intent = stripe.PaymentIntent.create(
    amount=content['amount'],
    currency="sgd",
    payment_method_types=["card"],
    receipt_email=content['cust_email'],
    stripe_account=content['stripe_account'],
    shipping=content['shipping']
    )

    return jsonify(intent)

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data

    try:
        event = json.loads(payload)
    except:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return jsonify(success=False)
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return jsonify(success=False)

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('Payment for {} succeeded'.format(payment_intent['amount']))
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)
