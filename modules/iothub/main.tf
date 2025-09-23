# IoT Hub (F1)
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

# Custom endpoint to route messages to Event Hub
resource "azurerm_iothub_endpoint_eventhub" "eh_endpoint" {
  name                = var.endpoint_name
  resource_group_name = var.resource_group_name
  iothub_id           = azurerm_iothub.this.id
  connection_string   = var.eh_send_connection_string
}

# Route device messages to the Event Hub endpoint
resource "azurerm_iothub_route" "eh_route" {
  name                = var.route_name
  resource_group_name = var.resource_group_name
  iothub_name         = azurerm_iothub.this.name
  source              = var.route_source
  condition           = var.route_condition
  endpoint_names      = [azurerm_iothub_endpoint_eventhub.eh_endpoint.name]
  enabled             = true
}

resource "azurerm_iothub_shared_access_policy" "iothubowner" {
  name                = "iothubowner1"
  resource_group_name = var.resource_group_name
  iothub_name         = azurerm_iothub.this.name

  registry_read   = true
  registry_write  = true
  service_connect = true
  device_connect  = true
}



