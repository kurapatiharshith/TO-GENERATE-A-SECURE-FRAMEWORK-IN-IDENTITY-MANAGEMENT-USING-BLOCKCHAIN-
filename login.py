import streamlit as st
import bcrypt
from wallet_connect import wallet_connect
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_CLIENT"))
db = client["PCL"]
users_collection = db["Users"]

def get_data(username, item):
    data = users_collection.distinct(item, {"username": username})

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Helper function to verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and verify_password(user["password"], password):
        return True
    return False

st.title("Login")
st.subheader("Login to your account", divider="rainbow")

username = st.text_input("Username")
address = st.text_input("Wallet Address")
password = st.text_input("Password", type="password")

# walletconnect = wallet_connect("Connect Wallet")
# if walletconnect:
#     st.session_state.meta = True

if st.button("Login"):
    if login_user(username, password):
        st.session_state.login = True
        st.session_state.username = username
        st.session_state.address = get_data(username, "address")
        st.success("Logged in successfully.")
        st.switch_page("Home")
    else:
        st.error("Invalid username or password or unrecognized wallet address.")