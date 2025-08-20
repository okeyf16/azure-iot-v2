variable "name" {
  type = string
  description = "IoT Hub name"
}

variable "resource_group_name" {
  type = string
  description = "Resource group for IoT Hub"
}

variable "location" {
  type = string
  description = "Region"
}

variable "tags" {
  type = map(string)
  default = {}
}

# Event Hub routing details
variable "endpoint_name" {
  type = string
}

variable "route_name" {
  type = string
}

variable "eh_send_connection_string" {
  type        = string
  sensitive   = true
}

variable "route_source" {
  type    = string
  default = "DeviceMessages"
}

variable "route_condition" {
  type    = string
  default = "true"
}
