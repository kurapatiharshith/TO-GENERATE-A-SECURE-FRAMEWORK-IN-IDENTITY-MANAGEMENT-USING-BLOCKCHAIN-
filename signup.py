import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Helper function to verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

load_dotenv()
client = MongoClient(os.getenv("MONGO_CLIENT"))
db = client["PCL"]
users_collection = db["Users"]

st.title("Signup")
st.subheader("Create an account", divider='rainbow')

def signup(username, password, address):
    if users_collection.find_one({"username": username}):
        return False
    
    hashed_password = hash_password(password)
    hashed_address = hash_password(address)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "address": hashed_address
    })
    return True

name = st.text_input("Username")
password = st.text_input("Password", type="password")
repeat_password = st.text_input("Repeat Password", type="password")
wallet_address = st.text_input("Wallet Address")
if st.button("Signup"):
    if password != repeat_password:
        st.error("Passwords do not match.")
    elif signup(name, password, wallet_address):
        st.success("Account created successfully.")
    else:
        st.error("Username already exists.")




    