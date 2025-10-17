output "resource_group"    { value = azurerm_resource_group.rg.name }
output "acr_name"          { value = azurerm_container_registry.acr.name }
output "container_app_url" { value = azurerm_container_app.api.latest_revision_fqdn }
output "search_endpoint"   { value = azurerm_search_service.search.query_endpoint }
output "kv_uri"            { value = azurerm_key_vault.kv.vault_uri }
