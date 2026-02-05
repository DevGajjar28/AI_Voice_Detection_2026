import requests
import base64
import json
import os

# Configuration
API_URL = "http://localhost:8000/api/voice-detection"
API_KEY = "sk_test_123456789"
AUDIO_FILE = "audio_samples/og.mp3"

def test_api():
    if not os.path.exists(AUDIO_FILE):
        print(f"Error: File {AUDIO_FILE} not found.")
        return

    # Read and encode audio
    with open(AUDIO_FILE, "rb") as f:
        audio_content = f.read()
        audio_base64 = base64.b64encode(audio_content).decode("utf-8")

    # Prepare payload
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    print(f"Sending request to {API_URL}...")
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Invalid API Key
    print("\n--- Test 2: Invalid API Key ---")
    headers_invalid = headers.copy()
    headers_invalid["x-api-key"] = "wrong_key"
    try:
        response = requests.post(API_URL, json=payload, headers=headers_invalid)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

    # Test 3: Invalid Audio Format
    print("\n--- Test 3: Invalid Audio Format ---")
    payload_invalid = payload.copy()
    payload_invalid["audioFormat"] = "wav" # strict mode allows only mp3
    try:
        response = requests.post(API_URL, json=payload_invalid, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
