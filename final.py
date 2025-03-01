from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "quiz11.json"

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Read existing data
def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Write new data
def write_data(new_entry):
    data = read_data()
    data.append(new_entry)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Route for homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")

# Route for quiz11
@app.route("/quiz11", methods=["GET", "POST"])
def quiz11():
    if request.method == "POST":
        user_data = request.json  # Receive JSON from frontend
        write_data(user_data)     # Store in JSON file
        return jsonify({"message": "Data saved successfully!"})

    return render_template("quiz11.html")  # Serve the quiz page

# Route to retrieve stored quiz data
@app.route("/get_quiz_data", methods=["GET"])
def get_quiz_data():
    return jsonify(read_data())

if __name__ == "__main__":
    app.run(debug=True)
