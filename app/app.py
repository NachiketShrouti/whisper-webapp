from flask import Flask, render_template, request
import os
import whisper

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model (you can switch "base" to any available size)
model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def upload():
    transcription = None
    if request.method == "POST":
        file = request.files.get("audio_file")
        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)
            result = model.transcribe(path)
            transcription = result["text"]
    return render_template("upload.html", transcription=transcription)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
