variable "name"                          { type = string }
variable "resource_group_name"           { type = string }
variable "location"                      { type = string }

variable "runtime_storage_account_name"  { type = string }
variable "runtime_storage_account_key"   { type = string }
variable "runtime_storage_connection_string" { type = string }

variable "eh_listen_connection_string"   { type = string }
variable "eventhub_name"                 { type = string }
variable "eh_consumer_group"             { type = string }

variable "data_storage_account_id"       { type = string }

variable "log_analytics_name"            { type = string }
variable "app_insights_name"             { type = string }
