import streamlit as st
from wallet_connect import wallet_connect

st.title("MetaMask Integration with Streamlit")

st.session_state.wallet = False

# Create a button to connect to MetaMask
connect_button = wallet_connect(label="wallet")

if connect_button:
    st.success("Wallet connected successfully!")
else:
    st.warning("Please connect your wallet.")
