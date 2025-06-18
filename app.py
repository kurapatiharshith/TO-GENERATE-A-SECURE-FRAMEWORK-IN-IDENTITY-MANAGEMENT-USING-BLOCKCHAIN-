import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_CLIENT"))
db = client["PCL"]
users_collection = db["Users"]

pages = {
    "DashBoard": [st.Page("home.py", title="Home"),
                  st.Page("about.py", title="Database")],
    "login/signup": [st.Page("login.py", title="Login"),
                     st.Page("signup.py", title="Signup")],
}

pg = st.navigation(pages)
pg.run()

if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = None

if "address" not in st.session_state:
    st.session_state.address = False

