import streamlit as st

st.title("Home")
st.write("This is the home page.")

col1, col2 = st.columns(2)

with col1:
  if st.button("Signup"):
    st.switch_page("signup.py")

with col2:
    if st.button("Login"):
        st.switch_page("login.py")

if st.button("Log-out"):
    st.session_state.login = False
    st.session_state.username = None
    st.session_state.address = None
    st.stop()