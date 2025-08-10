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
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            }
            with st.spinner("Processing..."):
                response = requests.post(f"{BACKEND_URL}/upload-pdf", files=files)
                if response.ok:
                    data = response.json()
                    st.success("PDF processed!")
                    st.subheader("Extracted Text")
                    st.text_area(
                        "",
                        data.get("extracted_text", ""),
                        height=600,
                    )
                    st.subheader("Summary")
                    st.text_area(
                        "",
                        data.get("summary", ""),
                        height=400,
                    )
                else:
                    st.error(f"Error: {response.status_code}")

with tab2:
    st.header("Enter a URL")
    url = st.text_input("Paste URL")

    if url and st.button("Submit URL"):
        with st.spinner("Fetching content..."):
            response = requests.post(f"{BACKEND_URL}/fetch-url", json={"url": url})
            if response.ok:
                data = response.json()
                st.success("Content fetched!")
                st.subheader("Extracted Text")
                st.text_area(
                    "",
                    data.get("text", ""),
                    height=300,
                )
                st.subheader("Summary")
                st.text_area(
                    "",
                    data.get("summary", ""),
                    height=200,
                )
            else:
                st.error(f"Error: {response.status_code}")
