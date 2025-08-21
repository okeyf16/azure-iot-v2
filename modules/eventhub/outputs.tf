output "send_connection_string"   { value = azurerm_eventhub_authorization_rule.sender.primary_connection_string }
output "listen_connection_string" { value = azurerm_eventhub_authorization_rule.listener.primary_connection_string }
output "eventhub_name"            { value = azurerm_eventhub.eh.name }
output "namespace_name"           { value = azurerm_eventhub_namespace.ns.name }

