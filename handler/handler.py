import base64
import traceback

def handler(event):
    try:
        audio_b64 = event['input']['audio_b64']
        filename = event['input'].get('filename', 'input.wav')

        print(f"Received audio with filename: {filename}")

        # Decode and write to file
        audio_bytes = base64.b64decode(audio_b64)
        with open(filename, "wb") as f:
            f.write(audio_bytes)

        print(f"Audio saved as {filename}")

        # Placeholder transcription logic
        transcription = "This is a placeholder transcription"

        return {"transcription": transcription}

    except Exception as e:
        print("Error occurred in handler:")
        traceback.print_exc()  # Show full error
        return {"error": str(e)}
