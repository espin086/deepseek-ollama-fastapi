# deepseek-ollama-fastapi

A Dockerized inference-serving layer: FastAPI/Uvicorn in front of Ollama running DeepSeek-R1, in a single container. Two endpoints cover the two ways a client needs a generation. synchronous (wait for the full response) and streaming (token-by-token over an open connection).

**Why streaming matters here:** a chat UI that waits for a full generation before showing anything reads as broken. The streaming endpoint keeps the HTTP connection open and flushes tokens as Ollama produces them, so the client can render output as it arrives instead of blocking on the slowest part of the request.

**Why one container instead of two services:** for a single-model deployment, running FastAPI and Ollama in the same container removes a network hop between them and simplifies the deploy surface to one image and one port mapping. It trades horizontal scalability of the two components independently for operational simplicity. the right tradeoff at this scale, wrong one past it.

**Relevant to:** inference-serving architecture, latency-sensitive API design (sync vs. streaming), containerized MLOps deployment.

### Benefits
- **All-in-One**: Runs FastAPI + Ollama in a single container.
- **Quick Deploy**: Build and run, no separate service orchestration needed.
- **LLM Ready**: Uses the DeepSeek `deepseek-r1:1.5b` model by default for text generation.
- **Easy to Extend**: Add new endpoints or swap models with minimal changes.

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
