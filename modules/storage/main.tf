resource "azurerm_storage_account" "this" {
  name                            = var.account_name
  resource_group_name             = var.resource_group_name
  location                        = var.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  account_kind                    = "StorageV2"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
}

resource "azurerm_storage_table" "tables" {
  for_each             = toset(var.tables)
  name                 = each.value
  storage_account_name = azurerm_storage_account.this.name
}

resource "azurerm_storage_table" "telemetry" {
  name                 = "TelemetryData"
  storage_account_name = azurerm_storage_account.this.name
  resource_group_name  = var.resource_group_name
}

