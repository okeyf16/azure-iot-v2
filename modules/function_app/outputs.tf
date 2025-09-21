output "name"                             { value = azurerm_linux_function_app.func.name }
output "principal_id"                     { value = azurerm_linux_function_app.func.identity[0].principal_id }

output "app_insights_instrumentation_key" {
  description = "The Instrumentation Key for Application Insights."
  value       = azurerm_application_insights.appinsights.instrumentation_key
  sensitive   = true
}

output "app_insights_connection_string" {
  description = "The Connection String for Application Insights."
  value       = azurerm_application_insights.appinsights.connection_string
  sensitive   = true
}
