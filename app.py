from flask import Flask, request, send_from_directory, render_template,jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["solar_database"]
collection = db["quiz_responses"]

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    if data:
        collection.insert_one(data)
        return jsonify({"message": "Data stored successfully"}), 201
    return jsonify({"error": "Invalid data"}), 400

# Configure the upload folder.
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Serve the HTML file (assume it's in the same directory or adjust as needed)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Endpoint to handle the image uploads.
@app.route('/upload', methods=['POST'])
def upload():
    if 'original_image' not in request.files or 'annotated_image' not in request.files:
        return 'Missing file(s)', 400

    original = request.files['original_image']
    annotated = request.files['annotated_image']

    original_filename = secure_filename(original.filename)
    annotated_filename = secure_filename(annotated.filename)

    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    annotated_path = os.path.join(app.config['UPLOAD_FOLDER'], annotated_filename)

    original.save(original_path)
    annotated.save(annotated_path)

    return 'Files uploaded successfully', 200

if __name__ == '_main_':
    app.run(debug=True)
