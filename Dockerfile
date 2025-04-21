FROM python:3.10-slim

# Install system deps: ffmpeg + git
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ffmpeg \
      git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies first
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install CPU version of PyTorch (optional if not using Whisper locally)
RUN pip install --no-cache-dir \
      torch \
      torchvision \
      torchaudio \
      --index-url https://download.pytorch.org/whl/cpu

# Whisper (optional if using Whisper locally; not needed if using RunPod only)
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Load environment variables from .env using python-dotenv
# Ensure .env file is copied ONLY for local use (use .dockerignore in real setup)
COPY .env .env

# Copy the actual Flask app
COPY app ./app

# Ensure upload directory exists and is writable
RUN mkdir -p /app/app/uploads && chmod -R 777 /app/app/uploads

WORKDIR /app/app

# Flask will load .env from root automatically via python-dotenv
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]