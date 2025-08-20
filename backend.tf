terraform {
  required_version = ">= 1.5.0"

  cloud {
    organization = "Octurion"
    workspaces {
      name = "azure-iot-v2"
    }
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}
