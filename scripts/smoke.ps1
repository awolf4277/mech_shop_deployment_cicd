param([string]$BaseUrl = "http://127.0.0.1:5000")
Write-Host "Pinging $BaseUrl/health ..."
try {
  $res = Invoke-RestMethod "$BaseUrl/health" -Method GET -TimeoutSec 10
  $ok = $res.ok -or $res.status -or $res -ne $null
  if ($ok) { Write-Host "Health OK ✅" -ForegroundColor Green } else { throw "Unexpected response" }
} catch {
  Write-Host "Health check failed ❌  $_" -ForegroundColor Red
  exit 1
}
