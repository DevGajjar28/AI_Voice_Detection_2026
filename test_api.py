import requests
import base64
import json
import numpy as np
import soundfile as sf
import io
import sys
import os

def create_silent_mp3():
    # Generate 1 second of silence
    sr = 22050
    y = np.zeros(sr)
    buffer = io.BytesIO()
    sf.write(buffer, y, sr, format='WAV')
    return buffer.getvalue()

def get_audio_bytes(file_path=None):
    if file_path:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
        print(f"Loading file: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()
    else:
        print("No file provided, generating silent audio for test...")
        return create_silent_mp3()

def test_api(file_path=None):
    url = "http://127.0.0.1:8000/api/voice-detection"
    api_key = "sk_test_123456789"
    
    audio_bytes = get_audio_bytes(file_path)
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Determine format from extension if file provided, else default to mp3 (or wav pretending to be mp3)
    audio_format = "mp3"
    if file_path:
        ext = os.path.splitext(file_path)[1].lower().replace('.', '')
        if ext:
            audio_format = ext

    payload = {
        "audioBase64": audio_base64,
        "language": "English", # Default language, can be changed or made an arg
        "audioFormat": audio_format
    }
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("-" * 30)
            print(f"RESULT: {result['classification']}")
            print(f"CONFIDENCE: {result['confidenceScore']}")
            print(f"EXPLANATION: {result['explanation']}")
            print("-" * 30)
            # print(f"Full Response: {json.dumps(result, indent=2)}")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if a file path argument is provided
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    test_api(file_path)
