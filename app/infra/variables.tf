variable "project" {
  type        = string
  description = "Project name"
}

variable "env" {
  type        = string
  description = "Environment (dev, staging, prod)"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "container_app_image" {
  type        = string
  default     = ""
  description = "Container image for the API app"
}

# Azure OpenAI Configuration
variable "openai_sku" {
  type        = string
  default     = "S0"
  description = "SKU for Azure OpenAI service"
}

variable "openai_deploy_chat" {
  type        = string
  default     = "gpt-4"
  description = "Deployment name for chat model"
}

variable "openai_deploy_embed" {
  type        = string
  default     = "text-embedding-ada-002"
  description = "Deployment name for embedding model"
}

variable "openai_chat_model_name" {
  type        = string
  default     = "gpt-4"
  description = "OpenAI chat model name"
}

variable "openai_chat_model_version" {
  type        = string
  default     = "0613"
  description = "OpenAI chat model version"
}

variable "openai_chat_capacity" {
  type        = number
  default     = 10
  description = "Capacity for chat deployment (in thousands of tokens per minute)"
}

variable "openai_embed_model_name" {
  type        = string
  default     = "text-embedding-ada-002"
  description = "OpenAI embedding model name"
}

variable "openai_embed_model_version" {
  type        = string
  default     = "2"
  description = "OpenAI embedding model version"
}

variable "openai_embed_capacity" {
  type        = number
  default     = 10
  description = "Capacity for embedding deployment (in thousands of tokens per minute)"
}

# Other Services
variable "redis_sku" {
  type        = string
  default     = "Basic"
  description = "SKU for Redis cache"
}

variable "search_sku" {
  type        = string
  default     = "basic"
  description = "SKU for Azure Cognitive Search"
}

variable "ingress_target_port" {
  type        = number
  default     = 8000
  description = "Target port for container app ingress"
}
