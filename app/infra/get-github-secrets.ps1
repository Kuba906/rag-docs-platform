# Script to get GitHub Actions secrets
# Run this from the app/infra directory after terraform apply

Write-Host "`n=== GitHub Actions Secrets ===" -ForegroundColor Cyan

# Get Terraform outputs
$ACR_NAME = terraform output -raw acr_name
$RG = terraform output -raw resource_group
$CONTAINER_APP_NAME = "$RG-api"

Write-Host "`n1. ACR_NAME:" -ForegroundColor Green
Write-Host $ACR_NAME

Write-Host "`n2. AZURE_RESOURCE_GROUP:" -ForegroundColor Green
Write-Host $RG

Write-Host "`n3. CONTAINER_APP_NAME:" -ForegroundColor Green
Write-Host $CONTAINER_APP_NAME

Write-Host "`n4. AZURE_CREDENTIALS:" -ForegroundColor Green
Write-Host "Run this command to generate:" -ForegroundColor Yellow
Write-Host "az ad sp create-for-rbac --name 'github-actions-rag-docs' --role contributor --scopes /subscriptions/a9f83a7f-8d64-4fda-a93e-f49b44e9129d/resourceGroups/$RG --sdk-auth" -ForegroundColor White

Write-Host "`n=== Grant ACR Access to Container App ===" -ForegroundColor Cyan
Write-Host "Run these commands:" -ForegroundColor Yellow

$PRINCIPAL_ID_CMD = "az containerapp show --name $CONTAINER_APP_NAME --resource-group $RG --query 'identity.principalId' -o tsv"
Write-Host "`n`$PRINCIPAL_ID = $PRINCIPAL_ID_CMD"

$ACR_ID_CMD = "az acr show --name $ACR_NAME --query id -o tsv"
Write-Host "`$ACR_ID = $ACR_ID_CMD"

Write-Host "az role assignment create --assignee `$PRINCIPAL_ID --role AcrPull --scope `$ACR_ID"

Write-Host "`n=== Add Secrets to GitHub ===" -ForegroundColor Cyan
Write-Host "Go to: https://github.com/YOUR-USERNAME/YOUR-REPO/settings/secrets/actions" -ForegroundColor Yellow
Write-Host "Add the 4 secrets listed above`n"
