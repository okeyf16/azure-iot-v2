output "send_connection_string"   { value = azurerm_eventhub_authorization_rule.sender.primary_connection_string }
output "listen_connection_string" { value = azurerm_eventhub_authorization_rule.listener.primary_connection_string }
output "eventhub_name"            { value = azurerm_eventhub.eh.name }
output "namespace_name"           { value = azurerm_eventhub_namespace.ns.name }
output "consumer_group"           { value = azurerm_eventhub_consumer_group.cg.name }

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
