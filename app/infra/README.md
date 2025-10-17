# Terraform — Project 2 (RAG)

Creates: RG, ACR, LAW, Container Apps Env + App (MI), Redis, Azure Cognitive Search, Key Vault, role assignment.

## Usage
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars -auto-approve

## After
- Put image into the Container App through CD (ACR) or set `container_app_image`.
- App should create **vector index** in Search on startup (docs, dim=1536).
