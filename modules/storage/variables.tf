variable "account_name"        { type = string }
variable "resource_group_name" { type = string }
variable "location"            { type = string }
variable "tables"              {
  type = list(string)
  default = [] 
}

