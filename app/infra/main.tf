data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "${local.name_prefix}-rg"
  location = var.location
}

resource "random_integer" "acr_suffix" {
  min = 1000
  max = 9999
}

resource "azurerm_container_registry" "acr" {
  name                = replace(lower("${local.name_prefix}acr${random_integer.acr_suffix.result}"), "-", "")
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}

# Azure OpenAI Cognitive Services Account
resource "azurerm_cognitive_account" "openai" {
  name                = "${local.name_prefix}-openai"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  kind                = "OpenAI"
  sku_name            = var.openai_sku

  custom_subdomain_name = replace(lower("${local.name_prefix}-openai"), "-", "")
}

# OpenAI Deployment for Chat (GPT-4)
resource "azurerm_cognitive_deployment" "chat" {
  name                 = var.openai_deploy_chat
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.openai_chat_model_name
    version = var.openai_chat_model_version
  }

  sku {
    name     = "Standard"
    capacity = var.openai_chat_capacity
  }
}

# OpenAI Deployment for Embeddings
resource "azurerm_cognitive_deployment" "embed" {
  name                 = var.openai_deploy_embed
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.openai_embed_model_name
    version = var.openai_embed_model_version
  }

  sku {
    name     = "Standard"
    capacity = var.openai_embed_capacity
  }
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

resource "random_integer" "redis_suffix" {
  min = 1000
  max = 9999
}
resource "azurerm_redis_cache" "redis" {
  name                 = "${local.name_prefix}-redis-${random_integer.redis_suffix.result}"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  capacity             = 0
  family               = "C"
  sku_name             = var.redis_sku
  non_ssl_port_enabled = false
}

resource "random_integer" "search_suffix" {
  min = 1000
  max = 9999
}
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
  key_vault_id       = azurerm_key_vault.kv.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = data.azurerm_client_config.current.object_id
  secret_permissions = ["Get", "List", "Set", "Delete"]
}

resource "azurerm_key_vault_secret" "openai_key" {
  name         = "AZURE-OPENAI-API-KEY"
  value        = azurerm_cognitive_account.openai.primary_access_key
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.deployer]
}

locals {
  redis_primary_key = azurerm_redis_cache.redis.primary_access_key
  redis_url         = "rediss://:${local.redis_primary_key}@${azurerm_redis_cache.redis.hostname}:6380/0"
}

resource "azurerm_key_vault_secret" "redis_url" {
  name         = "REDIS-URL"
  value        = local.redis_url
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.deployer]
}

data "azurerm_search_service" "search_data" {
  name                = azurerm_search_service.search.name
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_key_vault_secret" "search_key" {
  name         = "AZURE-SEARCH-ADMIN-KEY"
  value        = data.azurerm_search_service.search_data.primary_key
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.deployer]
}

resource "azurerm_container_app" "api" {
  name                         = "${local.name_prefix}-api"
  resource_group_name          = azurerm_resource_group.rg.name
  container_app_environment_id = azurerm_container_app_environment.cae.id
  revision_mode                = "Single"

  identity {
    type = "SystemAssigned"
  }

  template {
    min_replicas = 1
    max_replicas = 2

    container {
      name   = "api"
      image  = var.container_app_image != "" ? var.container_app_image : "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "APP_PORT"
        value = "8000"
      }
      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = azurerm_cognitive_account.openai.endpoint
      }
      env {
        name  = "AZURE_OPENAI_DEPLOYMENT_CHAT"
        value = azurerm_cognitive_deployment.chat.name
      }
      env {
        name  = "AZURE_OPENAI_DEPLOYMENT_EMBED"
        value = azurerm_cognitive_deployment.embed.name
      }
      env {
        name  = "AZURE_SEARCH_ENDPOINT"
        value = "https://${azurerm_search_service.search.name}.search.windows.net"
      }
      env {
        name  = "AZURE_SEARCH_INDEX"
        value = "docs"
      }

      env {
        name        = "REDIS_URL"
        secret_name = "redis-url"
      }
      env {
        name        = "AZURE_OPENAI_API_KEY"
        secret_name = "azure-openai-api-key"
      }
      env {
        name        = "AZURE_SEARCH_API_KEY"
        secret_name = "azure-search-api-key"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = var.ingress_target_port
    transport        = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  secret {
    name                = "azure-openai-api-key"
    identity            = "System"
    key_vault_secret_id = azurerm_key_vault_secret.openai_key.id
  }
  secret {
    name                = "redis-url"
    identity            = "System"
    key_vault_secret_id = azurerm_key_vault_secret.redis_url.id
  }
  secret {
    name                = "azure-search-api-key"
    identity            = "System"
    key_vault_secret_id = azurerm_key_vault_secret.search_key.id
  }
}

resource "azurerm_key_vault_access_policy" "api_mi_kv" {
  key_vault_id       = azurerm_key_vault.kv.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = azurerm_container_app.api.identity[0].principal_id
  secret_permissions = ["Get", "List"]
}

resource "azurerm_role_assignment" "api_mi_search_contrib" {
  scope                = azurerm_search_service.search.id
  role_definition_name = "Search Index Data Contributor"
  principal_id         = azurerm_container_app.api.identity[0].principal_id
}
