# Dockerfile (at repo root whisper-webapp/Dockerfile)
FROM python:3.10-slim

# (Optional) ffmpeg if you ever need to preprocess audio locally
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy & install client deps from app/requirements.txt
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Flask client code
COPY app ./app

# Create uploads dir
RUN mkdir -p /app/app/uploads && chmod -R 777 /app/app/uploads

WORKDIR /app/app

EXPOSE 5000

# Do NOT COPY .env; pass it at runtime with --env-file
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
