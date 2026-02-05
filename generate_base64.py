import base64
import pyperclip # pip install pyperclip

# File to convert
FILE_PATH = "audio_samples/og.mp3"

try:
    with open(FILE_PATH, "rb") as f:
        audio_content = f.read()
        base64_string = base64.b64encode(audio_content).decode("utf-8")
        
    print(f"Base64 string generated successfully!")
    print(f"Length: {len(base64_string)} characters")
    
    # Try to copy to clipboard
    try:
        pyperclip.copy(base64_string)
        print("✅ Copied to clipboard! You can paste it directly into Postman.")
    except:
        print("❌ Could not copy to clipboard. Please copy the output manually (saved to base64.txt).")
        with open("base64.txt", "w") as out:
            out.write(base64_string)
            print("Saved full string to 'base64.txt'")

except FileNotFoundError:
    print(f"Error: File {FILE_PATH} not found.")
