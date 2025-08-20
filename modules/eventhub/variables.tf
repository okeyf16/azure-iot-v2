variable "resource_group_name" { type = string }
variable "location"            { type = string }
variable "namespace_name"      { type = string }
variable "eventhub_name"       { type = string }
variable "throughput_units"    { type = number, default = 1 }
variable "partitions"          { type = number, default = 2 }
variable "retention_days"      { type = number, default = 1 }
variable "consumer_group"      { type = string, default = "func" }
