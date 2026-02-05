import base64
import os

# CONFIGURATION
# Replace this with your actual Render URL after deploying
API_URL = "https://your-app-name.onrender.com/api/voice-detection"
API_KEY = "sk_test_123456789"
AUDIO_FILE = "audio_samples/og.mp3"
OUTPUT_FILE = "curl_test_command.txt"

def create_curl_command():
    if not os.path.exists(AUDIO_FILE):
        print(f"Error: Audio file '{AUDIO_FILE}' not found.")
        return

    # 1. Convert Audio to Base64
    with open(AUDIO_FILE, "rb") as f:
        audio_content = f.read()
        base64_string = base64.b64encode(audio_content).decode("utf-8")

    # 2. Construct the cURL command
    # We use a heredoc format for the data to handle the long string cleanly in some shells,
    # but for maximum compatibility (Windows/Linux), we'll put it in a standard -d flag 
    # taking care to escape quotes if needed. 
    # Since it's JSON, we'll write it to a file and tell curl to read from file using @
    
    json_payload = f'''{{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "{base64_string}"
}}'''

    # Save payload to a file (best practice for large data)
    payload_filename = "payload.json"
    with open(payload_filename, "w") as f:
        f.write(json_payload)
    print(f"✅ Generated '{payload_filename}' with audio data.")

    # 3. Create the command to run
    # Windows Command Prompt compatible
    curl_cmd = f'curl -X POST "{API_URL}" -H "Content-Type: application/json" -H "x-api-key: {API_KEY}" -d @{payload_filename}'

    with open(OUTPUT_FILE, "w") as f:
        f.write(curl_cmd)

    print(f"✅ Generated '{OUTPUT_FILE}' containing the full command.")
    print("\n--- HOW TO USE ---")
    print(f"1. Open '{OUTPUT_FILE}'")
    print("2. Replace 'your-app-name.onrender.com' with your actual deployed URL.")
    print("3. Copy and paste the command into your terminal.")

if __name__ == "__main__":
    create_curl_command()
