output "name"         { value = azurerm_linux_function_app.func.name }
output "principal_id" { value = azurerm_linux_function_app.func.identity[0].principal_id }
