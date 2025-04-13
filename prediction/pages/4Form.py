import streamlit as st
import requests
import numpy as np
import joblib  # Import for loading ML model

# Load the trained model
classifier = joblib.load("autism_model.pkl")

st.title(":bookmark_tabs: :blue[Autism Data Assessment]")
st.write("---")
st.write("Fill the form below to check if your child is suffering from ASD.")

# Function to map input values
def ValueCount(str):
    return 1 if str == "Yes" else 0

def Sex(str):
    return 1 if str == "Female" else 0

# Input Fields
name = st.text_input("Enter Child's Name")
val1 = st.selectbox("Social Responsiveness", list(range(11)))
val2 = st.selectbox("Age", list(range(19)))
val3 = ValueCount(st.selectbox("Speech Delay", ["No", "Yes"]))
val4 = ValueCount(st.selectbox("Learning Disorder", ["No", "Yes"]))
val5 = ValueCount(st.selectbox("Genetic Disorders", ["No", "Yes"]))
val6 = ValueCount(st.selectbox("Depression", ["No", "Yes"]))
val7 = ValueCount(st.selectbox("Intellectual Disability", ["No", "Yes"]))
val8 = ValueCount(st.selectbox("Social/Behavioural Issues", ["No", "Yes"]))
val9 = ValueCount(st.selectbox("Anxiety Disorder", ["No", "Yes"]))
val10 = Sex(st.selectbox("Gender", ["Female", "Male"]))
val11 = ValueCount(st.selectbox("Suffers from Jaundice", ["No", "Yes"]))
val12 = ValueCount(st.selectbox("Family Member History with ASD", ["No", "Yes"]))
val13 = st.selectbox("IQ Level", [70, 80, 90, 100, 110, 120, 130])
val14 = ValueCount(st.selectbox("Motor Coordination Issues", ["No", "Yes"]))
val15 = ValueCount(st.selectbox("Attention Span Issues", ["No", "Yes"]))
val16 = ValueCount(st.selectbox("Sleeping Disorders", ["No", "Yes"]))
val17 = ValueCount(st.selectbox("Emotional Sensitivity", ["No", "Yes"]))
val18 = ValueCount(st.selectbox("Hyperactivity", ["No", "Yes"]))


# Update input data list
input_data = [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12,
              val13, val14, val15, val16, val17, val18]

if st.button("Submit"):
    # Convert input to NumPy array
    input_data_as_numpy_array = np.asarray(input_data).reshape(1, -1)

    # Make prediction
    prediction = classifier.predict(input_data_as_numpy_array)[0]
    result = "Autistic" if prediction == 1 else "Not Autistic"

    # Display result
    with st.expander("Analyze provided data"):
        st.subheader("Results:")
        if result == "Autistic":
            st.warning(f'{name} is likely to have Autism Spectrum Disorder. Please consult a specialist.')
        else:
            st.info(f'{name} is not likely to have Autism Spectrum Disorder.')

    # Send data to backend
    response = requests.post("http://127.0.0.1:5000/predict", json={
        "name": name,
        "features": input_data,
        "prediction": result
    })

    if response.status_code == 200:
        st.success("Prediction successfully saved to the database!")
    else:
        st.error("Error: Unable to save data.")
