$root = Split-Path $PSScriptRoot -Parent
. "$root\env.ps1"
az search service delete -n $SEARCH -g $RG --yes
Write-Host "Search deleted. Hourly billing stopped." -ForegroundColor Green
