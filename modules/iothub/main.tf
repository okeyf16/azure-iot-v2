# IoT Hub
resource "azurerm_iothub" "this" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name

  sku {
    name     = "F1"
    capacity = 1
  }

  tags = var.tags
}

# Event Hub custom endpoint for routing
resource "azurerm_iothub_endpoint_eventhub" "eh_endpoint" {
  name                = var.endpoint_name
  iothub_name         = azurerm_iothub.this.name
  resource_group_name = var.resource_group_name
  connection_string   = var.eh_send_connection_string
}

# IoT Hub route to Event Hub endpoint
resource "azurerm_iothub_route" "eh_route" {
  name                = var.route_name
  iothub_name         = azurerm_iothub.this.name
  resource_group_name = var.resource_group_name

  source              = var.route_source
  condition           = var.route_condition
  endpoint_names      = [azurerm_iothub_endpoint_eventhub.eh_endpoint.name]
  enabled             = true
}
