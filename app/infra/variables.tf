variable "project" { type = string }
variable "env"     { type = string }
variable "location"{ type = string }
variable "container_app_image" { type = string, default = "" }
variable "openai_endpoint"     { type = string }
variable "openai_api_key"      { type = string, sensitive = true }
variable "openai_deploy_chat"  { type = string }
variable "openai_deploy_embed" { type = string }
variable "redis_sku"  { type = string, default = "Basic" }
variable "search_sku" { type = string, default = "basic" }
variable "ingress_target_port" { type = number, default = 8000 }
