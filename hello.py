from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

DATA_FILE = "data.json"

def load_data():
    """Load existing data from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_data(data):
    """Save new data to the JSON file."""
    existing_data = load_data()
    existing_data.append(data)
    with open(DATA_FILE, "w") as file:
        json.dump(existing_data, file, indent=4)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    save_data(data)
    return jsonify({"message": "Data stored successfully!"})

if __name__ == '__main__':
    app.run(debug=True)