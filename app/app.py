import os
import base64
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Now access the environment variables
RUNPOD_API_KEY  = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT = os.getenv("RUNPOD_ENDPOINT")

# Check if variables are loaded correctly
print("RUNPOD_API_KEY:", RUNPOD_API_KEY)
print("RUNPOD_ENDPOINT:", RUNPOD_ENDPOINT)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    transcription = None
    error = None

    if request.method == "POST":
        file = request.files.get("audio_file")
        if not file:
            error = "No file uploaded."
        else:
            # save locally (optional)
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            # encode to base64 so we can send via JSON
            with open(path, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode("utf-8")

            # prepare payload
            payload = {
                "input": {
                    "audio_b64": audio_b64,
                    "filename": file.filename
                }
            }
            headers = {"Authorization": f"Bearer {RUNPOD_API_KEY}"}
            try:
                resp = requests.post(RUNPOD_ENDPOINT, headers=headers, json=payload)
                resp.raise_for_status()
                transcription = resp.json().get("transcription")
            except requests.exceptions.RequestException as e:
                error = f"Request error: {e}"
                if resp is not None:
                   error += f" - Response: {resp.text}"    
            except Exception as e:
                error = f"RunPod error: {e}"

    return render_template("upload.html",
                           transcription=transcription,
                           error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
