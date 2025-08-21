resource "azurerm_eventhub_namespace" "ns" {
  name                = var.namespace_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Basic"
  capacity            = var.throughput_units
  auto_inflate_enabled = false
}

resource "azurerm_eventhub" "eh" {
  name                = var.eventhub_name
  namespace_name      = azurerm_eventhub_namespace.ns.name
  resource_group_name = var.resource_group_name
  partition_count     = var.partitions
  message_retention   = var.retention_days
}

resource "azurerm_eventhub_authorization_rule" "sender" {
  name                = "sender"
  eventhub_name       = azurerm_eventhub.eh.name
  namespace_name      = azurerm_eventhub_namespace.ns.name
  resource_group_name = var.resource_group_name
  listen              = false
  send                = true
  manage              = false
}

resource "azurerm_eventhub_authorization_rule" "listener" {
  name                = "listener"
  eventhub_name       = azurerm_eventhub.eh.name
  namespace_name      = azurerm_eventhub_namespace.ns.name
  resource_group_name = var.resource_group_name
  listen              = true
  send                = false
  manage              = false
}

