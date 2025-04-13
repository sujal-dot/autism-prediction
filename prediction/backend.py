from flask import Flask, request, jsonify
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load your trained model
model = pickle.load(open('model.pkl', 'rb'))
scaler = StandardScaler()  # If you used scaling in training, load it here

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)  # Get JSON input
    input_data = np.array(data['features']).reshape(1, -1)  # Convert to NumPy array
    
    # Preprocess data if needed
    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)  # Make prediction
    return jsonify({'prediction': prediction.tolist()})  # Return JSON response

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask server
