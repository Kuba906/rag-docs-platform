output "resource_group" {
  value       = azurerm_resource_group.rg.name
  description = "Resource group name"
}

output "acr_name" {
  value       = azurerm_container_registry.acr.name
  description = "Azure Container Registry name"
}

output "container_app_url" {
  value       = azurerm_container_app.api.latest_revision_fqdn
  description = "Container App URL"
}

output "openai_endpoint" {
  value       = azurerm_cognitive_account.openai.endpoint
  description = "Azure OpenAI endpoint"
}

output "openai_chat_deployment" {
  value       = azurerm_cognitive_deployment.chat.name
  description = "OpenAI chat deployment name"
}

output "openai_embed_deployment" {
  value       = azurerm_cognitive_deployment.embed.name
  description = "OpenAI embedding deployment name"
}

output "search_endpoint" {
  value       = "https://${azurerm_search_service.search.name}.search.windows.net"
  description = "Azure Cognitive Search endpoint"
}

output "kv_uri" {
  value       = azurerm_key_vault.kv.vault_uri
  description = "Key Vault URI"
}
