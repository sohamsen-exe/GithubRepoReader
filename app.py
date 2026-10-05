import streamlit as st
import requests

st.set_page_config(page_title="Repo Explainer", layout="centered")

st.title("Gen AI Mini Assessment - GitHub Repo Explainer")
st.write("Enter a GitHub URL to generate a explanation entirely offline.")

url = st.text_input("Repository URL:", placeholder="https://github.com/username/repository")

if st.button("Explain Repository"):
    if url:
        with st.spinner("Cloning repository and generating explanation..."):
            try:
                response = requests.post("https://modified-mumbo-footman.ngrok-free.dev/explain", json={"url": url})
                
                if response.status_code == 200:
                    explanation = response.json().get("explanation", "")
                    st.success("Analysis Complete!")
                    st.markdown(explanation)
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to backend. Is FastAPI running?")
    else:
        st.warning("Please enter a valid GitHub repository URL.")