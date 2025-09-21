output "id"                        { value = azurerm_storage_account.this.id }
output "name"                      { value = azurerm_storage_account.this.name }
output "primary_connection_string" { value = azurerm_storage_account.this.primary_connection_string }
output "primary_access_key"        { value = azurerm_storage_account.this.primary_access_key }
output "telemetry_table_name"      { value = azurerm_storage_table.telemetry.name }  #new#


