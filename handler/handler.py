import runpod, whisper, base64, tempfile, os

# load model once into GPU memory
model = whisper.load_model("base")

def handler(job):
    inp = job["input"]
    audio_b64 = inp.get("audio_b64")
    filename  = inp.get("filename", "input.wav")
    if not audio_b64:
        return {"error": "No audio_b64 in input"}

    # write temp file
    data = base64.b64decode(audio_b64)
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1], delete=False) as tf:
        tf.write(data)
        tmp_path = tf.name

    # transcribe
    res = model.transcribe(tmp_path)
    os.remove(tmp_path)
    return {"transcription": res["text"]}

# start serverless worker
runpod.serverless.start({"handler": handler})
