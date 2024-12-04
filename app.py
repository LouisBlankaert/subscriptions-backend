from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
CORS(app)

# Données fictives d'abonnements
subscriptions = []

# Fonction pour obtenir le logo automatiquement via Clearbit
def get_logo_url(name):
    base_url = "https://logo.clearbit.com/"
    domain = f"{name.lower()}.com"  # Génère un domaine approximatif
    return f"{base_url}{domain}"

# Récupérer tous les abonnements
@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    return jsonify(subscriptions)

# Ajouter un abonnement
@app.route('/subscriptions', methods=['POST'])
def add_subscription():
    data = request.json
    logo_url = get_logo_url(data.get('name'))  # Appel automatique de la fonction de logo
    new_subscription = {
        "id": len(subscriptions) + 1,
        "name": data.get('name'),
        "price": data.get('price'),
        "isActive": data.get('isActive'),
        "logoUrl": logo_url  # URL du logo
    }
    subscriptions.append(new_subscription)
    return jsonify({"message": "Subscription added!", "subscription": new_subscription}), 201

# Supprimer un abonnement
@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    global subscriptions
    subscriptions = [s for s in subscriptions if s["id"] != subscription_id]
    return jsonify({"message": "Subscription deleted!"})

# Adapter pour Vercel (serverless)
def handler(environ, start_response):
    from werkzeug.wsgi import DispatcherMiddleware
    application = DispatcherMiddleware(app)
    return application(environ, start_response)

# Le code principal reste inchangé. 
# Flask sera utilisé en mode serverless sur Vercel sans SharedDataMiddleware.
