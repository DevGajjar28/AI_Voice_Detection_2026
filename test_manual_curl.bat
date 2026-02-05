@echo off
REM This file is for manually testing the live API with curl on Windows.
REM It handles the escaping correctly so you don't have to type it.

echo Sending request to live server...
curl -X POST "https://ai-voice-detection-2026.onrender.com/api/voice-detection" ^
 -H "Content-Type: application/json" ^
 -H "x-api-key: sk_test_123456789" ^
 -d "{\"language\":\"Tamil\", \"audioFormat\":\"mp3\", \"audioBase64\":\"SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAA\"}"

echo.
echo.
pause
