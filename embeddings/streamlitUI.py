import streamlit as st
import requests

# Title of the app
st.title("Application Management Service")

# Input fields to take user data
#key = st.text_input("Enter Key")
value = st.text_input("Enter Value")

# Button to submit data
if st.button('Submit'):
    # Creating the JSON payload
    payload = {
      #  "key": key,
        "query": value
    }

    # Send the request to your Flask API (or any other API)
    response = requests.post("http://localhost:5000/search", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        st.success("Data successfully submitted")
        st.json(response.json())  # Display the JSON response
    else:
        st.error("Failed to submit data")
