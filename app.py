from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Données fictives d'abonnements
subscriptions = []

# Fonction pour obtenir le logo automatiquement via Clearbit
def get_logo_url(name):
    base_url = "https://logo.clearbit.com/"
    domain = f"{name.lower()}.com"  # Génère un domaine approximatif
    return f"{base_url}{domain}"

# Redirection de la racine vers /subscriptions
@app.route('/')
def home():
    return redirect('/subscriptions')

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

if __name__ == '__main__':
    app.run(debug=True)
