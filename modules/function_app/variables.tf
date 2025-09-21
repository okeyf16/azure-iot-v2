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

variable "telemetry_table_name" {
  type        = string
  description = "Name of the Azure Table Storage table"
}

variable "storage_account_id" {
  type        = string
  description = "ID of the storage account to assign permissions to"
}

variable "storage_account_data_connection_string" {
  type        = string
  description = "Connection string for the telemetry data storage account"
  sensitive   = true
}

variable "log_analytics_workspace_id" {
  type        = string
  description = "Log Analytics Workspace ID for Application Insights"
}

variable "tags" {
  type    = map(string)
  description = "Tags for resources"
}

variable "app_insights_name" {
  type        = string
  description = "Name of the Application Insights instance"
}






