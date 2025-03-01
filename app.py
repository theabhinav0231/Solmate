from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ✅ Correct MongoDB Connection
MONGO_URI = "mongodb+srv://meenakshi16rp:E5vMBg7qG27fHUL8@cluster0.tbaqr.mongodb.net/Cluster0?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Cluster0"]  # Ensure correct database
collection = db["user_responses"]  # Ensure correct collection

# Routes for HTML pages
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/quiz11')
def quiz1():
    return render_template('quiz11.html')

@app.route('/quiz2')
def quiz2():
    return render_template('quiz22.html')

@app.route('/quiz3')
def quiz3():
    return render_template('quiz33.html')

@app.route('/quiz5')
def quiz5():
    return render_template('quiz55.html')

@app.route('/quiz6')
def quiz6():
    return render_template('quiz66.html')

@app.route('/quiz7')
def quiz7():
    return render_template('quiz77.html')

@app.route('/quiz8')
def quiz8():
    return render_template('quiz88.html')

# ✅ Save Location API
@app.route('/save_location', methods=['POST'])
def save_location():
    try:
        data = request.json
        print("📥 Received Data:", data)  # Debugging print

        user_id = data.get('user_id', str(ObjectId()))  # Ensure string user_id
        print("🆔 User ID:", user_id)  # Debugging print
        result = collection.insert_one({
            'user_id': user_id,
            'location': data.get('location'),
            'timestamp': datetime.now()
        })

        print(f"✅ Data inserted with _id: {result.inserted_id}")
        return jsonify({'success': True, 'user_id': user_id}), 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

# ✅ Save Roof Area API
@app.route('/save_roof_area', methods=['POST'])
def save_roof_area():
    try:
        data = request.json
        user_id = data.get('user_id', str(ObjectId()))
        roof_area = float(data.get('roof_area', 0))

        result = collection.update_one(
            {'user_id': user_id},
            {'$set': {'roof_area': roof_area, 'timestamp': datetime.now()}},
            upsert=True
        )
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Save Electricity Consumption API
@app.route('/save_electricity_consumption', methods=['POST'])
def save_electricity_consumption():
    try:
        data = request.json
        user_id = data.get('user_id', str(ObjectId()))
        consumption = int(data.get('consumption', 0))

        result = collection.update_one(
            {'user_id': user_id},
            {'$set': {'electricity_consumption': consumption, 'timestamp': datetime.now()}},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Save Electricity Rate API
@app.route('/save_electricity_rate', methods=['POST'])
def save_electricity_rate():
    try:
        data = request.json
        user_id = data.get('user_id', str(ObjectId()))
        rate = float(data.get('rate', 0))

        result = collection.update_one(
            {'user_id': user_id},
            {'$set': {'electricity_rate': rate, 'timestamp': datetime.now()}},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Save Storage Preference API
@app.route('/save_storage_preference', methods=['POST'])
def save_storage_preference():
    try:
        data = request.json
        user_id = data.get('user_id', str(ObjectId()))
        storage_preference = data.get('storage_preference', '')

        result = collection.update_one(
            {'user_id': user_id},
            {'$set': {'storage_preference': storage_preference, 'timestamp': datetime.now()}},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Save Budget API
@app.route('/save_budget', methods=['POST'])
def save_budget():
    try:
        data = request.json
        user_id = data.get('user_id', str(ObjectId()))
        budget = int(data.get('budget', 0))

        result = collection.update_one(
            {'user_id': user_id},
            {'$set': {'budget': budget, 'timestamp': datetime.now(), 'form_completed': True}},
            upsert=True
        )
        return jsonify({'success': True, 'message': 'Form completed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Get All User Responses API
@app.route('/api/user_responses', methods=['GET'])
def get_user_responses():
    try:
        responses = list(collection.find({}))
        for response in responses:
            response['_id'] = str(response['_id'])
        return jsonify(responses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Get a Specific User's Response API
@app.route('/api/user_responses/<user_id>', methods=['GET'])
def get_user_response(user_id):
    try:
        response = collection.find_one({'user_id': user_id})
        if not response:
            return jsonify({'error': 'User not found'}), 404
        response['_id'] = str(response['_id'])
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
