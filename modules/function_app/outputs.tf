output "name"                             { value = azurerm_linux_function_app.func.name }
output "principal_id"                     { value = azurerm_linux_function_app.func.identity[0].principal_id }
output "app_insights_instrumentation_key" { value = azurerm_application_insights.ai.instrumentation_key }
output "app_insights_connection_string"   { value = azurerm_application_insights.ai.connection_string }


