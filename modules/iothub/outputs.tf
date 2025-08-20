
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

