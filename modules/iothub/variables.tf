variable "resource_group_name" {
  description = local.rg_name
  type = string
}

variable "location"            {
  description = var.location
  type = string
}

variable "namespace_name"      {
  description = local.eh_namespace_name
  type = string
}

variable "eventhub_name"       {
  description = local.eh_name
  type = string
}

variable "eh_endpoint_name" {
  description = local.eh_endpoint_name
  type        = string
}

variable "eh_route_name" {
  description = local.eh_route_name 
  type        = string
}

variable "eh_send_connection_string" {
  description = module.eventhub.send_connection_string
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


