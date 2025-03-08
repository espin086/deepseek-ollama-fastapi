from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os
import config

app = FastAPI()


class PromptRequest(BaseModel):
    """
    PromptRequest is a Pydantic model that defines the structure of the request body for the /generate endpoint.
    It includes a prompt field, which is a string, and a stream field, which is a boolean.
    """
    prompt: str
    stream: bool = False

@app.post("/generate")
async def generate_response(request: PromptRequest):
    """
    generate_response is an asynchronous FastAPI endpoint that generates a response to a given prompt.
    It uses the Ollama API to generate the response.
    """
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model":'deepseek-r1:1.5b',
        "prompt": request.prompt,
        "stream": request.stream
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Ollama API error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Ollama: {str(e)}")

# Optional: Add a streaming endpoint if needed
@app.post("/generate/stream")
async def generate_stream(request: PromptRequest):
    """
    generate_stream is an asynchronous FastAPI endpoint that generates a streaming response to a given prompt.
    It uses the Ollama API to generate the streaming response.
    """
    from fastapi.responses import StreamingResponse
    
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": 'deepseek-r1:1.5b',
        "prompt": request.prompt,
        "stream": True
    }
    
    async def generate():
        """
        generate is an asynchronous function that generates a streaming response to a given prompt.
        It uses the Ollama API to generate the streaming response.
        """
        try:
            response = requests.post(url, json=data, stream=True)
            for line in response.iter_lines():
                if line:
                    yield line + b'\n'
        except requests.exceptions.RequestException as e:
            yield json.dumps({"error": str(e)}).encode() + b'\n'
    
    return StreamingResponse(generate(), media_type="application/x-ndjson") 