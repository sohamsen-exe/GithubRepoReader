import streamlit as st
import os
import tempfile
import shutil
from git import Repo
from groq import Groq

# Initialize Groq client using Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_repo_context(repo_url: str) -> str:
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(repo_url, temp_dir)
        allowed_extensions = ['.py', '.js', '.jsx', '.html', '.css', '.md', '.json']
        combined_code = ""
        
        for root, dirs, files in os.walk(temp_dir):
            if '.git' in root:
                continue
            for file in files:
                if any(file.endswith(ext) for ext in allowed_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            combined_code += f"\n\n--- File: {file} ---\n\n"
                            combined_code += f.read()
                    except Exception:
                        continue
        return combined_code[:15000]
    finally:
        shutil.rmtree(temp_dir)

st.set_page_config(page_title="Repo Explainer", layout="centered")
st.title("Cloud GitHub Repository Explainer")

url = st.text_input("Repository URL:", placeholder="https://github.com/username/repository")

if st.button("Explain Repository"):
    if url:
        with st.spinner("Cloning repository and analyzing codebase..."):
            try:
                code_context = get_repo_context(url)
                if not code_context:
                    st.error("No readable code found in the repository.")
                else:
                    system_prompt = (
                        "Analyze the following codebase. You must output your response using exactly these three sections:\n"
                        "1. Project Overview\n"
                        "2. Main Technologies (as a bulleted list)\n"
                        "3. How it works\n\n"
                        f"Codebase:\n{code_context}"
                    )
                    
                    # Using a lightweight LLaMA model hosted on Groq
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b", # Updated model name
                        messages=[{"role": "user", "content": system_prompt}]
                    )
                    
                    st.success("Analysis Complete!")
                    st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a valid GitHub repository URL.")
