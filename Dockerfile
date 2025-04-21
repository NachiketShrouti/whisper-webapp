FROM python:3.10-slim

# Install system deps: ffmpeg + git
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ffmpeg \
      git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements (Flask listed here)
COPY requirements.txt .

# Install CPU PyTorch
RUN pip install --no-cache-dir \
      torch \
      torchvision \
      torchaudio \
      --index-url https://download.pytorch.org/whl/cpu

# Install Whisper from GitHub
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Install Flask
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app

WORKDIR /app/app

# Expose port and launch
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
