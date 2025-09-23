
output "name" {
  value = azurerm_iothub.this.name
}

output "id" {
  value = azurerm_iothub.this.id
}

output "route_name" {
  value = azurerm_iothub_route.eh_route.name
}

output "endpoint_name" {
  value = azurerm_iothub_endpoint_eventhub.eh_endpoint.name
}

output "connection_string" {
  value     = azurerm_iothub_shared_access_policy.iothubowner.primary_connection_string
  sensitive = true
}

