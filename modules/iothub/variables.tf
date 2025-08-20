variable "name" {
  type        = string
  description = "Name of the IoT Hub"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group in which to create the IoT Hub"
}

variable "location" {
  type        = string
  description = "Azure region for IoT Hub"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Optional tags"
}

# Event Hub endpoint config
variable "endpoint_name" {
  type        = string
  description = "Name of the Event Hub endpoint within IoT Hub"
}

variable "route_name" {
  type        = string
  description = "Name of the route in IoT Hub"
}

variable "namespace_name" {
  type        = string
  description = "Event Hub namespace name"
}

variable "eventhub_name" {
  type        = string
  description = "Event Hub name"
}

variable "eh_send_connection_string" {
  type        = string
  sensitive   = true
  description = "Event Hub send policy connection string including EntityPath"
}

variable "route_source" {
  type        = string
  default     = "DeviceMessages"
  description = "Source of the messages in IoT Hub routing (e.g., DeviceMessages)"
}

variable "route_condition" {
  type        = string
  default     = "true"
  description = "Condition for the route (optional expression)"
}
