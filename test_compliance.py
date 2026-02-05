import requests
import base64
import json
import numpy as np
import soundfile as sf
import io

def create_silent_mp3():
    sr = 22050
    y = np.zeros(sr)
    buffer = io.BytesIO()
    sf.write(buffer, y, sr, format='WAV')
    return buffer.getvalue()

def run_test(name, payload, headers, expected_status):
    url = "http://127.0.0.1:8000/api/voice-detection"
    print(f"--- Test: {name} ---")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
        
        if response.status_code == expected_status:
            print("PASS")
        else:
            print(f"FAIL (Expected {expected_status})")
            
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    audio_bytes = create_silent_mp3()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    valid_key = "sk_test_123456789"
    
    # 1. Valid Request
    run_test(
        "Valid Request (Tamil)",
        {"language": "Tamil", "audioFormat": "mp3", "audioBase64": audio_base64},
        {"x-api-key": valid_key},
        200
    )
    
    # 2. Invalid Language
    run_test(
        "Invalid Language (French)",
        {"language": "French", "audioFormat": "mp3", "audioBase64": audio_base64},
        {"x-api-key": valid_key},
        400
    )
    
    # 3. Invalid Format
    run_test(
        "Invalid Format (wav)",
        {"language": "English", "audioFormat": "wav", "audioBase64": audio_base64},
        {"x-api-key": valid_key},
        400
    )
    
    # 4. Invalid API Key
    run_test(
        "Invalid API Key",
        {"language": "English", "audioFormat": "mp3", "audioBase64": audio_base64},
        {"x-api-key": "wrong-key"},
        401
    )
