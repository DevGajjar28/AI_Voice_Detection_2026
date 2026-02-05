$url = "https://ai-voice-detection-2026.onrender.com/api/voice-detection"
$key = "sk_test_123456789"
$payloadFile = "payload.json"

Write-Host "Testing Live API at: $url"

if (-not (Test-Path $payloadFile)) {
    Write-Error "File '$payloadFile' not found in current directory! Please ensure you are in the correct folder and have run the generator script."
    exit 1
}

# We use curl.exe explicitly to bypass the PowerShell alias 'curl' -> 'Invoke-WebRequest'
# We quote "@payload.json" to prevent PowerShell from interpreting '@' as a splatting operator
& curl.exe -X POST "$url" -H "Content-Type: application/json" -H "x-api-key: $key" -d "@$payloadFile"
