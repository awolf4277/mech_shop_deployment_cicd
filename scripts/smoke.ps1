# scripts/smoke.ps1
param([string]$Base = "http://127.0.0.1:5000")

Write-Host "🚦 Smoke against $Base" -ForegroundColor Cyan

function J {
  param(
    [string]$u,
    [string]$m = "GET",
    [hashtable]$h = @{},
    [string]$b = $null
  )
  try {
    if ($b) {
      Invoke-RestMethod $u -Method $m -Headers $h -ContentType "application/json" -Body $b | ConvertTo-Json -Depth 6
    } else {
      Invoke-RestMethod $u -Method $m -Headers $h | ConvertTo-Json -Depth 6
    }
  } catch {
    Write-Host "HTTP error for $m $u" -ForegroundColor Red
    if ($_.Exception.Response -and $_.Exception.Response.StatusCode.Value__) {
      $_.Exception.Response.StatusCode.Value__
    }
  }
}

# Public GETs
J "$Base/health"
J "$Base/customers/"
J "$Base/mechanics/"
J "$Base/mechanics/top"
J "$Base/inventory/"
J "$Base/service-tickets/"

# Login for JWT
$login   = @{ email="admin@example.com"; password="admin123" } | ConvertTo-Json
$resp    = Invoke-RestMethod "$Base/auth/login" -Method Post -ContentType "application/json" -Body $login
$token   = $resp.access_token
$headers = @{ Authorization = "Bearer $token" }

# Unique customer (avoid duplicate email)
$r    = Get-Random
$cust = @{ name="User$r"; email="user$r@example.com"; password="pass123" } | ConvertTo-Json
J "$Base/customers/" "POST" @{} $cust

# Mechanic
$mech = @{ name="Ava"; specialty="Transmissions"; rating=4.7 } | ConvertTo-Json
J "$Base/mechanics/" "POST" @{} $mech

# Inventory
$item = @{ part_name="Oil Filter"; quantity=10; unit_price=8.50 } | ConvertTo-Json
J "$Base/inventory/" "POST" @{} $item

# Ticket + edit
$ticket  = @{ customer_id=1; vehicle="2015 Honda Accord"; issue="Brake noise"; status="open" } | ConvertTo-Json
$created = Invoke-RestMethod "$Base/service-tickets/" -Method Post -ContentType "application/json" -Body $ticket
$edit    = @{ status="in_progress" } | ConvertTo-Json
J "$Base/service-tickets/$($created.id)/edit" "PUT" @{} $edit

# Lists again
J "$Base/service-tickets/my-tickets"
J "$Base/customers/"
J "$Base/inventory/"

Write-Host "✅ Smoke completed." -ForegroundColor Green
