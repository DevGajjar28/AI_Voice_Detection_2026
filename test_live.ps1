# Use script directory so this works when run from anywhere (e.g. C:\Users\DEV)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$payloadFile = Join-Path $ScriptDir "payload.json"
$url = "https://ai-voice-detection-2026.onrender.com/api/voice-detection"
$key = "sk_test_123456789"

Write-Host "Testing Live API at: $url"
Write-Host "Payload file: $payloadFile"

if (-not (Test-Path $payloadFile)) {
    Write-Error "File '$payloadFile' not found. Generate it with generate_base64.py or create_curl_test.py in the project folder."
    exit 1
}

# curl.exe: @file must be the path so curl reads from that path (not PowerShell splatting)
& curl.exe -X POST $url -H "Content-Type: application/json" -H "x-api-key: $key" -d "@$payloadFile"
