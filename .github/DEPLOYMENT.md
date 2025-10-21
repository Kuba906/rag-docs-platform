# Deployment Guide - GitHub Actions CI/CD

This document describes how to configure automatic deployment to Azure using GitHub Actions.

## Prerequisites

- Azure infrastructure created by Terraform (Resource Group, ACR, Container App)
- GitHub repository
- Azure CLI installed locally

## Step 1: Get Resource Information from Terraform

Execute in the `app/infra` directory:

```bash
cd app/infra

# Get ACR name
terraform output acr_name

# Get Resource Group name
terraform output resource_group

# Container App name (default)
# rag-dev-api
```

## Step 2: Create Service Principal in Azure

Service Principal is a "user account" for GitHub Actions to authenticate with Azure.

```bash
# Get subscription ID
az account show --query id -o tsv

# Create Service Principal (replace SUBSCRIPTION_ID with actual ID)
az ad sp create-for-rbac \
  --name "github-actions-rag-platform" \
  --role contributor \
  --scopes /subscriptions/SUBSCRIPTION_ID \
  --sdk-auth
```

**IMPORTANT:** Copy the entire JSON output - you'll need it in the next step!

The output looks like this:
```json
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx",
  ...
}
```

## Step 3: Add GitHub Secrets

1. Go to: https://github.com/Kuba906/rag-docs-platform/settings/secrets/actions

2. Click **New repository secret** and add the following secrets:

### Secret 1: AZURE_CREDENTIALS
- **Name:** `AZURE_CREDENTIALS`
- **Value:** The entire JSON output from step 2 (Service Principal)

### Secret 2: ACR_NAME
- **Name:** `ACR_NAME`
- **Value:** ACR name from `terraform output acr_name` (e.g., `ragdevacr1234`)

### Secret 3: AZURE_RESOURCE_GROUP
- **Name:** `AZURE_RESOURCE_GROUP`
- **Value:** Resource Group name from `terraform output resource_group` (e.g., `rag-dev-rg`)

### Secret 4: CONTAINER_APP_NAME
- **Name:** `CONTAINER_APP_NAME`
- **Value:** Container App name (default: `rag-dev-api`)

## Step 4: Grant ACR Permissions to Service Principal

The Service Principal needs permission to push images to ACR:

```bash
# Get Service Principal Client ID from JSON output in step 2
SP_CLIENT_ID="xxx"  # clientId from JSON

# Get ACR name
ACR_NAME=$(cd app/infra && terraform output -raw acr_name)

# Grant permissions
az role assignment create \
  --assignee $SP_CLIENT_ID \
  --role AcrPush \
  --scope /subscriptions/$(az account show --query id -o tsv)/resourceGroups/$(cd app/infra && terraform output -raw resource_group)/providers/Microsoft.ContainerRegistry/registries/$ACR_NAME
```

## Step 5: Test Deployment

1. Commit and push the workflow:
```bash
git add .github/
git commit -m "Add GitHub Actions CI/CD workflow"
git push
```

2. Go to: https://github.com/Kuba906/rag-docs-platform/actions

3. Monitor the progress - deployment should take 3-5 minutes

## How Does It Work?

After every push to `master` or `main`:

1. GitHub Actions builds the Docker image
2. Authenticates with Azure Container Registry
3. Pushes the image to ACR with tags (git commit SHA + latest)
4. Updates Container App to use the new image
5. Displays the application URL

## Manual Execution

You can also run the workflow manually:
1. Go to the Actions tab in GitHub
2. Select "Build and Deploy to Azure"
3. Click "Run workflow"

## Troubleshooting

### Error: "Error: The subscription is not registered to use namespace Microsoft.ContainerRegistry"
```bash
az provider register --namespace Microsoft.ContainerRegistry
```

### Error: "unauthorized: authentication required"
Check if the Service Principal has AcrPush permissions (step 4)

### Error: "Container App not found"
Verify that the Container App name in GitHub Secrets is correct

## Monitoring

After deployment, check application logs:

```bash
# Get Resource Group and Container App name
RG_NAME=$(cd app/infra && terraform output -raw resource_group)
APP_NAME="rag-dev-api"

# View logs
az containerapp logs show \
  --name $APP_NAME \
  --resource-group $RG_NAME \
  --follow
```

## Rollback

If the new deployment has issues, you can revert to a previous version:

```bash
# List revisions
az containerapp revision list \
  --name $APP_NAME \
  --resource-group $RG_NAME \
  --output table

# Activate previous revision
az containerapp revision activate \
  --name $APP_NAME \
  --resource-group $RG_NAME \
  --revision REVISION_NAME
```
