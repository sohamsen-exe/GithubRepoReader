import os
import tempfile
import shutil
from git import Repo

def get_repo_context(repo_url: str) -> str:
    # Create a temporary directory for cloning
    temp_dir = tempfile.mkdtemp()
    
    try:
        Repo.clone_from(repo_url, temp_dir)
        
        # Define the file extensions you want the LLM to read
        allowed_extensions = ['.py', '.js', '.jsx', '.html', '.css', '.md', '.json']
        combined_code = ""
        
        # Traverse the cloned directory
        for root, dirs, files in os.walk(temp_dir):
            # Skip the hidden .git folder
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
                        continue # Skip unreadable files
                        
        # Truncate the string to prevent exceeding the local model's context window
        return combined_code[:15000]
        
    finally:
        # Ensure the temporary directory is deleted after extraction
        shutil.rmtree(temp_dir)