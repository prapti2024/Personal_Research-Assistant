import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # Update if deployed elsewhere

st.title("📚 Personal Research Assistant")

tab1, tab2 = st.tabs(["Upload PDF", "Fetch from URL"])

with tab1:
    st.header("Upload a PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Submit PDF"):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            with st.spinner("Processing..."):
                response = requests.post(f"{BACKEND_URL}/upload-pdf", files=files)
                if response.ok:
                    st.success("PDF processed!")
                    st.text_area("Extracted Text", response.json().get("text", ""), height=300)
                else:
                    st.error(f"Error: {response.status_code}")

with tab2:
    st.header("Enter a URL")
    url = st.text_input("Paste URL")

    if st.button("Submit URL"):
        with st.spinner("Fetching content..."):
            response = requests.post(f"{BACKEND_URL}/fetch-url", json={"url": url})
            if response.ok:
                st.success("Content fetched!")
                st.text_area("Extracted Text", response.json().get("text", ""), height=300)
            else:
                st.error(f"Error: {response.status_code}")
