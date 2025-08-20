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

