import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import time
import requests
from streamlit_lottie import st_lottie
import hashlib
import sqlite3

st.set_page_config(layout="wide")

# Security
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        menu_title="Start Here!",
        options=["Signup", "Login"],
        icons=["box-seam-fill", "box-seam-fill"],
        menu_icon="home",
        default_index=0
    )

# Signup Section
if selected == "Signup":
    st.title(":iphone: :blue[Create New Account]")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user, make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

# Login Section
elif selected == "Login":
    st.title(":calling: :blue[Login Section]")
    username = st.text_input("User Name")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username, check_hashes(password, hashed_pswd))
        prog = st.progress(0)
        for per_comp in range(100):
            time.sleep(0.05)
            prog.progress(per_comp + 1)
        if result:
            st.success(f"Logged In as {username}")
            st.warning("Go to Dashboard!")

            # Collect User Inputs for Prediction
            st.subheader(":bar_chart: Enter Details for Autism Prediction")
            age = st.number_input("Age", min_value=1, max_value=100)
            gender = st.selectbox("Gender", ["Male", "Female"])
            score = st.slider("Score", min_value=0, max_value=100)

            # Prepare user input data
            gender_numeric = 1 if gender == "Male" else 0  # Convert gender to numeric

            user_input = [age, gender_numeric, score]  # Now age, gender, score are defined

            if st.button("Predict"):
                # Send data to Flask backend
                response = requests.post("http://127.0.0.1:5000/predict", json={"features": user_input})
                if response.status_code == 200:
                    prediction = response.json().get('prediction')
                    st.success(f"Prediction: {prediction}")
                else:
                    st.error("Failed to get prediction from the backend.")
        else:
            st.warning("Incorrect Username/Password")
