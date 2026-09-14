$root = Split-Path $PSScriptRoot -Parent
. "$root\env.ps1"

az search service create -n $SEARCH -g $RG -l $LOC --sku basic --partition-count 1 --replica-count 1 --identity-type SystemAssigned -o none
az search service update -n $SEARCH -g $RG --auth-options aadOrApiKey --aad-auth-failure-mode http401WithBearerChallenge -o none

$ME        = az ad signed-in-user show --query id -o tsv
$SR_ID     = az search service show -n $SEARCH -g $RG --query id -o tsv
$SEARCH_MI = az search service show -n $SEARCH -g $RG --query identity.principalId -o tsv
$ST_ID     = az storage account show -n $STORAGE -g $RG --query id -o tsv
$AI_ID     = az cognitiveservices account show -n $AISVC -g $RG --query id -o tsv
$UAMI_ID   = az identity show -n $UAMI -g $RG --query principalId -o tsv

az role assignment create --assignee $ME        --role "Search Service Contributor"     --scope $SR_ID -o none
az role assignment create --assignee $ME        --role "Search Index Data Contributor"  --scope $SR_ID -o none
az role assignment create --assignee $UAMI_ID   --role "Search Index Data Contributor"  --scope $SR_ID -o none
az role assignment create --assignee $SEARCH_MI --role "Storage Blob Data Reader"       --scope $ST_ID -o none
az role assignment create --assignee $SEARCH_MI --role "Cognitive Services OpenAI User" --scope $AI_ID -o none

az search service show -n $SEARCH -g $RG --query "{Name:name, Sku:sku.name, Status:status, Semantic:semanticSearch}" -o json
Write-Host "Search is up. Wait ~2 min for RBAC, then run: python -m backend.search.index_schema" -ForegroundColor Green
