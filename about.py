import streamlit as st
import pandas as pd

if st.session_state.login == False:
    st.error("You are not logged in. Please log in to access this page.")
    st.stop()

st.title("Database")

data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [25, 30, 35, 28],
    "Occupation": ["Engineer", "Doctor", "Artist", "Scientist"]
}

df = pd.DataFrame(data)
st.subheader("Data", divider='rainbow')
st.table(df)


