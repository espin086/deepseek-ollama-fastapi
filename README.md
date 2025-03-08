# deepseek-ollama-fastapi
A Docker-based solution for running the Deep Seek LLM via Ollama, exposed by a FastAPI application using Uvicorn. This repo includes straightforward endpoints for both synchronous and streaming text-generation requests, making it easy to integrate the “deepseek-r1” model into your own applications.


### ✨ Benefits
- 🚀 **All-in-One**: Runs FastAPI + Ollama in a **single container**.
- ⚡ **Quick Deploy**: Just build and run—no complicated setup.
- 🎯 **LLM Ready**: Uses the Deep Seek `deepseek-r1:1.5b` model by default for text generation.
- 🏗 **Easy to Extend**: Add new endpoints or swap models with minimal changes.

---

### 🐳 Build & Run with Docker

1. **Clone this repo**:
 ```bash
 git clone https://github.com/your-username/deepseek-ollama-fastapi.git
 cd deepseek-ollama-fastapi
 ```
2. **Build the image (replace MODEL_NAME if you want a different model on Ollama)**:

 ```bash
docker build -t deepseek-ollama-fastapi:latest \
  --build-arg MODEL_NAME=deepseek-r1:1.5b .
```

3. **Run the container**:
```bash
docker run -it --rm \
    -p 8000:8000 \
    -p 11434:11434 \
    --name deepseek-ollama \
    deepseek-ollama-fastapi:latest
```

⚙️ Quick Test (Local)


Synchronous

```bash
curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Hello DeepSeek!", "stream":false}'
```


Streaming

```bash
curl -X POST http://localhost:8000/generate/stream \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Stream me some AI wisdom!", "stream":true}'

```

