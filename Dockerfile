FROM ubuntu:22.04

# Add build argument for model name with a default value
ARG MODEL_NAME=deepseek-r1:1.5b
ENV MODEL_NAME=${MODEL_NAME}

# Install curl, Python, and pip
RUN apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in the background, pull the model, and then stop Ollama
RUN ollama serve & \
    sleep 5 && \
    ollama pull ${MODEL_NAME} && \
    pkill ollama

# Copy your FastAPI application
COPY app.py /app/app.py

# Set working directory
WORKDIR /app

# Expose both Ollama and FastAPI ports
EXPOSE 11434 8000

# Start both Ollama and FastAPI
CMD ollama serve & uvicorn app:app --host 0.0.0.0 --port 8000 