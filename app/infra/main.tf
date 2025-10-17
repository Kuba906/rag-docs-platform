data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" { name = "${local.name_prefix}-rg" location = var.location }

resource "azurerm_container_registry" "acr" {
  name                = replace(lower("${local.name_prefix}acr"), "-", "")
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = "${local.name_prefix}-law"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "cae" {
  name                       = "${local.name_prefix}-cae"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
}

resource "random_integer" "redis_suffix" { min = 1000 max = 9999 }
resource "azurerm_redis_cache" "redis" {
  name                = "${local.name_prefix}-redis-${random_integer.redis_suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  capacity            = 0
  family              = "C"
  sku_name            = var.redis_sku
  enable_non_ssl_port = false
}

resource "random_integer" "search_suffix" { min = 1000 max = 9999 }
resource "azurerm_search_service" "search" {
  name                = "${local.name_prefix}-search-${random_integer.search_suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = var.search_sku
}

resource "azurerm_key_vault" "kv" {
  name                       = replace(lower("${local.name_prefix}-kv"), "-", "")
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
}

resource "azurerm_key_vault_access_policy" "deployer" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id
  secret_permissions = ["Get","List","Set","Delete"]
}

resource "azurerm_key_vault_secret" "openai_key" { name = "AZURE-OPENAI-API-KEY" value = var.openai_api_key key_vault_id = azurerm_key_vault.kv.id }

locals { redis_primary_key = azurerm_redis_cache.redis.primary_access_key
         redis_url = "rediss://:${local.redis_primary_key}@${azurerm_redis_cache.redis.hostname}:6380/0" }

resource "azurerm_key_vault_secret" "redis_url" { name = "REDIS-URL" value = local.redis_url key_vault_id = azurerm_key_vault.kv.id }

data "azurerm_search_service" "search_data" {
  name                = azurerm_search_service.search.name
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_key_vault_secret" "search_key" {
  name         = "AZURE-SEARCH-ADMIN-KEY"
  value        = data.azurerm_search_service.search_data.primary_key
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_container_app" "api" {
  name                         = "${local.name_prefix}-api"
  resource_group_name          = azurerm_resource_group.rg.name
  container_app_environment_id = azurerm_container_app_environment.cae.id
  revision_mode                = "Single"

  identity { type = "SystemAssigned" }

  template {
    container {
      name   = "api"
      image  = var.container_app_image != "" ? var.container_app_image : "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.5
      memory = "1Gi"

      env { name = "APP_PORT" value = "8000" }
      env { name = "AZURE_OPENAI_ENDPOINT" value = var.openai_endpoint }
      env { name = "AZURE_OPENAI_DEPLOYMENT_CHAT" value = var.openai_deploy_chat }
      env { name = "AZURE_OPENAI_DEPLOYMENT_EMBED" value = var.openai_deploy_embed }
      env { name = "AZURE_SEARCH_ENDPOINT" value = azurerm_search_service.search.query_endpoint }
      env { name = "AZURE_SEARCH_INDEX" value = "docs" }

      env { name = "REDIS_URL" secret_name = azurerm_key_vault_secret.redis_url.name }
      env { name = "AZURE_OPENAI_API_KEY" secret_name = azurerm_key_vault_secret.openai_key.name }
      env { name = "AZURE_SEARCH_API_KEY" secret_name = azurerm_key_vault_secret.search_key.name }
    }
    scale { min_replicas = 1 max_replicas = 2 }
  }

  ingress { external_enabled = true target_port = var.ingress_target_port transport = "auto" }

  secret { name = azurerm_key_vault_secret.openai_key.name identity = "System" key_vault_secret_id = azurerm_key_vault_secret.openai_key.id }
  secret { name = azurerm_key_vault_secret.redis_url.name identity = "System" key_vault_secret_id = azurerm_key_vault_secret.redis_url.id }
  secret { name = azurerm_key_vault_secret.search_key.name identity = "System" key_vault_secret_id = azurerm_key_vault_secret.search_key.id }
}

resource "azurerm_key_vault_access_policy" "api_mi_kv" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_container_app.api.identity[0].principal_id
  secret_permissions = ["Get","List"]
}

resource "azurerm_role_assignment" "api_mi_search_contrib" {
  scope                = azurerm_search_service.search.id
  role_definition_name = "Search Index Data Contributor"
  principal_id         = azurerm_container_app.api.identity[0].principal_id
}
