variable "name" {
  description = "Web App name"
  type        = string
}

variable "plan_name" {
  description = "App Service Plan name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "app_insights_key" {
  description = "App Insights instrumentation key"
  type        = string
}

variable "app_insights_conn_string" {
  description = "App Insights connection string"
  type        = string
}

variable "storage_conn_str" {
  description = "Storage account connection string"
  type        = string
}

variable "api_key" {
  description = "API Key for backend auth"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
