from flask import Flask, request, jsonify
import joblib
import numpy as np
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("autism_model.pkl")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["autism_db"]
collection = db["predictions"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    if "features" not in data or "name" not in data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        # Store prediction in MongoDB
        collection.insert_one({
            "name": data["name"],
            "features": data["features"],
            "prediction": data["prediction"]
        })

        return jsonify({"message": "Prediction saved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
