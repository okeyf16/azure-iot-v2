terraform {
  backend "remote" {
    organization = "Octurion"
    workspaces {
      name = "azure-iot-v2"
    }
  }
}
