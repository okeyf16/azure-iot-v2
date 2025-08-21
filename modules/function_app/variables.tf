variable "name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "storage_account_access_key" {
  type      = string
  sensitive = true
}

variable "eventhub_listen_conn_string" {
  type      = string
  sensitive = true
}

variable "eventhub_name" {
  type = string
}

variable "table_name" {
  type = string
}

variable "storage_account_id" {
  type = string
}

variable "log_analytics_workspace_id" {
  type        = string
  description = "Log Analytics Workspace ID for Application Insights"
}

variable "tags" {
  type    = map(string)
  default = {}
}

