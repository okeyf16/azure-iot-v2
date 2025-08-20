variable "ARM_CLIENT_ID" {
  type        = string
  description = "92243d42-ca4b-4baf-885e-1ed8a7542eb7"
  sensitive   = true
}

variable "ARM_CLIENT_SECRET" {
  type        = string
  description = "gMM8Q~abXIt33zBccRW0rQ~EnEO7d~h8jvPwpahJ"
  sensitive   = true 
}

variable "ARM_SUBSCRIPTION_ID" {
  type        = string
  description = "9112a04a-6011-49f2-904c-f2b66b865b40"
}

variable "ARM_TENANT_ID" {
  type        = string
  description = "1bac489a-6766-481d-ace8-a72c1b526435"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "North Europe"
}

variable "resource_group_name" {
  type    = string
  default = "iot-gen-ehub"
}


variable "tags" {
  type = map(string)
  default = {
    project = "iot-ehub-func"
  }
}

variable "iothub_name" {
  type    = string
  default = "hub30906"
}

variable "eh_endpoint_name" {
  type    = string
  default = "eh-endpoint"
}

variable "eh_route_name" {
  type    = string
  default = "route-device-msgs"
}

variable "eventhub_namespace_name" {
  type    = string
  default = "ehns-iot-basic"
}

variable "eventhub_name" {
  type    = string
  default = "telemetry"
}

variable "storage_account_data_name" {
  type    = string
  default = "sttelemetrydata123" # Must be globally unique
}

variable "storage_account_func_name" {
  type    = string
  default = "stfuncstoragedev123" # Must be globally unique
}

variable "table_name" {
  type    = string
  default = "telemetry"
}

variable "function_app_name" {
  type    = string
  default = "fn-iot-ehub"
}

