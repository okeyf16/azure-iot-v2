variable "name" {
  type        = string
  description = "Name of the Log Analytics Workspace"
}

variable "location" {
  type        = string
  description = "Azure Region"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group for the workspace"
}

variable "sku" {
  type        = string
  default     = "PerGB2018"
}

variable "retention_in_days" {
  type        = number
  default     = 30
}

variable "tags" {
  type        = map(string)
  description = "Tags for the workspace"
}
