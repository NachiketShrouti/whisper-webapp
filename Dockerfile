FROM python:3.10-slim

# Install system deps: ffmpeg + git
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ffmpeg \
      git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install CPU PyTorch (move before Whisper to make installation clearer)
RUN pip install --no-cache-dir \
      torch \
      torchvision \
      torchaudio \
      --index-url https://download.pytorch.org/whl/cpu

# Install Whisper from GitHub (move it last)
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Permissions update
RUN mkdir -p /app/uploads && chmod -R 777 /app/uploads

# Copy app code
COPY app ./app

WORKDIR /app/app

# Expose port and launch Flask app
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
