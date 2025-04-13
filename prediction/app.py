import numpy as np
import joblib

# Load the model and scaler
model = joblib.load('/Users/sujal/Desktop/autism/prediction/autism_model.pkl')
scaler = joblib.load('/Users/sujal/Desktop/autism/prediction/scaler.pkl')

# Define a function for prediction
def predict_autism(input_data):
    # Convert input to numpy array
    input_data = np.asarray(input_data)
    
    # Reshape the input for one sample
    input_data_reshaped = input_data.reshape(1, -1)
    
    # Standardize input
    std_data = scaler.transform(input_data_reshaped)
    
    # Make prediction
    prediction = model.predict(std_data)
    
    # Return the result
    if prediction[0] == 0:
        return "The person is not with Autism Spectrum Disorder."
    else:
        return "The person is with Autism Spectrum Disorder."

# Example input
example_input = (0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0)
result = predict_autism(example_input)
print(result)
