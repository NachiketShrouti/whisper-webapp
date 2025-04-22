import base64
import os

def handler(event):
    try:
        # Extract base64 encoded audio and optional filename
        audio_b64 = event['input']['audio_b64']
        filename = event['input'].get('filename', 'input.wav')

        # Print for debugging
        print(f"Received audio with filename: {filename}")

        # Decode base64 and save the audio file
        audio_bytes = base64.b64decode(audio_b64)
        with open(filename, "wb") as f:
            f.write(audio_bytes)

        print(f"Audio saved as {filename}")

        # Add transcription logic here, for now return a dummy result
        transcription = "This is a placeholder transcription"

        # Return transcription
        return {"transcription": transcription}

    except Exception as e:
        print("Error occurred in handler:", str(e))
        return {"error": str(e)}
