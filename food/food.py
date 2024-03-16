from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# Dummy database to store food donations
food_donations = []

# Dummy database to store users (businesses and charities)
users = {}

# Routes for businesses to donate food
@app.route('/donate', methods=['POST'])
def donate_food():
    data = request.json
    business_id = data.get('business_id')
    food_items = data.get('food_items')
    timestamp = datetime.now()

    donation = {
        'donation_id': str(uuid.uuid4()),
        'business_id': business_id,
        'food_items': food_items,
        'timestamp': timestamp
    }

    food_donations.append(donation)
    return jsonify({'message': 'Food donation successful', 'donation_id': donation['donation_id']}), 201

# Route for charities to request food
@app.route('/request_food', methods=['POST'])
def request_food():
    data = request.json
    charity_id = data.get('charity_id')
    requested_items = data.get('requested_items')

    # Logic to match requested items with available donations
    matched_donations = []

    for donation in food_donations:
        if all(item in donation['food_items'] for item in requested_items):
            matched_donations.append(donation)

    # For simplicity, just return all matched donations
    return jsonify({'matched_donations': matched_donations}), 200

# Route to create user accounts
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    user_id = str(uuid.uuid4())
    user_type = data.get('user_type')  # 'business' or 'charity'
    # For simplicity, assume user provides username and password for registration
    username = data.get('username')
    password = data.get('password')
    
    users[user_id] = {
        'user_type': user_type,
        'username': username,
        'password': password
    }

    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201

if __name__ == '__main__':
    app.run(debug=True)
