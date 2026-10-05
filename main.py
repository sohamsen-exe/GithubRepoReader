from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
from extractor import get_repo_context

app = FastAPI()

class RepoRequest(BaseModel):
    url: str

@app.post("/explain")
async def explain_repo(request: RepoRequest):
    try:
        # Extract the code from the provided GitHub URL
        code_context = get_repo_context(request.url)
        
        if not code_context:
            raise HTTPException(status_code=400, detail="No readable code found in the repository.")
            
        # Construct the prompt enforcing the required output structure
        system_prompt = (
            "Analyze the following codebase. You must output your response using exactly these three sections:\n"
            "1. Project Overview\n"
            "2. Main Technologies (as a bulleted list)\n"
            "3. How it works\n\n"
            f"Codebase:\n{code_context}"
        )
        
        # Call the local model
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt}
        ])
        
        return {"explanation": response['message']['content']}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))