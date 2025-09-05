# Navigate to your Flask project folder
Set-Location "C:\Users\Admin\OneDrive - United States International University (USIU)\Desktop\USIU MAp Project"

# Set Flask app environment variable
$env:FLASK_APP = "app.py"

# Start Flask in the background
Start-Process powershell -ArgumentList "flask run --host=0.0.0.0 --port=5000"

# Wait a few seconds for Flask to start
Start-Sleep -Seconds 3

# Start ngrok in the background
Start-Process powershell -ArgumentList "ngrok http 5000"

# Wait for ngrok to establish tunnel
Start-Sleep -Seconds 5

# Fetch the public ngrok HTTPS URL from its API
try {
    $response = Invoke-RestMethod -Uri http://127.0.0.1:4040/api/tunnels
    $url = $response.tunnels | Where-Object {$_.public_url -like "https://*"} | Select-Object -ExpandProperty public_url
    
    Write-Host ""
    Write-Host "🚀 Your app is running online:"
    Write-Host "   User link : $url"
    Write-Host "   Admin link: $url/login"
    Write-Host ""

    # Open User link in default browser
    Start-Process $url
} catch {
    Write-Host "❌ Failed to fetch ngrok URL. Is ngrok running?"
}
