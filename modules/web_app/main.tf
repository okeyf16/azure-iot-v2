#######################
# App Service Plan    #
#######################
resource "azurerm_service_plan" "this" {
  name                = var.plan_name
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type = "Linux" 
  sku_name = "F1"
  }
}

#######################
# Web App             #
#######################
resource "azurerm_app_service" "this" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  app_service_plan_id = azurerm_app_service_plan.this.id

  site_config {
    always_on = false # Free tier does not support Always On
  }

  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = var.app_insights_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = var.app_insights_conn_string
    "STORAGE_CONN_STR"                      = var.storage_conn_str
    "API_KEY"                               = var.api_key
  }

  tags = var.tags
}
