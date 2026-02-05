@echo off
REM Run from anywhere: uses payload.json in the same folder as this .bat
cd /d "%~dp0"

if not exist payload.json (
    echo payload.json not found in %~dp0
    echo Generate it with generate_base64.py or create_curl_test.py first.
    pause
    exit /b 1
)

echo Sending request to live server...
curl.exe -X POST "https://ai-voice-detection-2026.onrender.com/api/voice-detection" -H "Content-Type: application/json" -H "x-api-key: sk_test_123456789" -d "@payload.json"

echo.
pause
