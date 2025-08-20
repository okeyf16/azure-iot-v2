variable "resource_group_name" {
  description = "iot-gen-ehub"
  type = string
}

variable "location"            {
  description = "North Europe"
  type = string
}

variable "namespace_name"      {
  description = "ehub30906"
  type = string
}

variable "eventhub_name"       {
  description = "ehub1"
  type = string
}

variable "eh_endpoint_name" {
  description = "eh-endpoint"
  type        = string
}

variable "eh_route_name" {
  description = "route-to-eh" 
  type        = string
}

variable "eh_send_connection_string" {
  description = "The connection string for the Event Hub endpoint."
  type        = string
  sensitive   = true
}

variable "throughput_units"    {
  type = number
  default = 1 
}

variable "partitions"          {
  type = number
  default = 2
}

variable "retention_days"      {
  type = number
  default = 1 
}

variable "consumer_group"      {
  type = string
  default = "func" 
}

variable "name" {
  type = string
}

variable "endpoint_name" {
  type = string
}

variable "route_name" {
  type = string
}

variable "eh_send_connection_string" {
  type = string
}




