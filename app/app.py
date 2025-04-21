import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Read RunPod endpoint & API key from environment
RUNPOD_URL = os.getenv("RUNPOD_URL")
API_KEY    = os.getenv("RUNPOD_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def upload():
    transcription = None
    if request.method == 'POST':
        file = request.files.get('audio_file')
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            # Send to RunPod GPU endpoint
            with open(filepath, 'rb') as f:
                files = {'file': f}
                headers = {
                    'accept': 'application/json',
                    'authorization': API_KEY
                }
                resp = requests.post(RUNPOD_URL, headers=headers, files=files)

            # ✅ Debug output
            print("📡 RunPod Response Status Code:", resp.status_code)
            print("📄 RunPod Response Text:", resp.text)
            print("🧪 RUNPOD_URL from env:", RUNPOD_URL)


            try:
                data = resp.json()
                transcription = data.get('output', {}).get('text')
            except Exception as e:
                print("❌ JSON decode error:", e)
                transcription = "Error: Could not parse response from RunPod."

    return render_template('upload.html', transcription=transcription)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
