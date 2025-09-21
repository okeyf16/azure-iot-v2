resource "azurerm_service_plan" "plan" {
  name                = "${var.name}-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "Y1" # Consumption

  tags = var.tags
}

resource "azurerm_application_insights" "ai" {
  name                = var.app_insights_name
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
  workspace_id        = var.log_analytics_workspace_id
  tags                = var.tags
}


resource "azurerm_linux_function_app" "func" {
  name                       = var.name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  service_plan_id            = azurerm_service_plan.plan.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key

  identity {
    type = "SystemAssigned"
}

lifecycle {
  ignore_changes = [
    # This is set by the deployment pipeline (e.g., GitHub Actions)
    app_settings["WEBSITE_RUN_FROM_PACKAGE"]
    ]
  }

  site_config {
    application_stack {
      python_version = "3.11"  # Or "3.10", "3.9" depending on your code
    }

    ftps_state          = "Disabled"
    minimum_tls_version = "1.2"

   # Add missing settings from the live configuration
    scm_type                       = "GitHubAction"
    function_app_scale_limit       = 200
    minimum_elastic_instance_count = 1

  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME         = "python"
    FUNCTIONS_EXTENSION_VERSION      = "~4"
    # WEBSITE_RUN_FROM_PACKAGE         = "1" #reccomended for removal by gemini during repo/code harmonization

    # Bindings
    EventHubConnection               = var.eventhub_listen_conn_string
    EVENT_HUB_NAME                   = var.eventhub_name

    # Storage
    #TABLE_NAME                       = var.table_name
    TELEMETRY_TABLE_NAME              = var.telemetry_table_name
    TelemetryStorage                  = var.storage_account_data_connection_string

    # App Insights
    APPINSIGHTS_INSTRUMENTATIONKEY       = azurerm_application_insights.ai.instrumentation_key
    APPLICATIONINSIGHTS_CONNECTION_STRING = azurerm_application_insights.ai.connection_string
  }

  tags = var.tags
}

# Allow MSI to write to Table Storage (sa_data)
data "azurerm_role_definition" "table_data_contrib" {
  name  = "Storage Table Data Contributor"
  scope = var.storage_account_id
}

resource "azurerm_role_assignment" "table_access" {
  principal_id       = azurerm_linux_function_app.func.identity[0].principal_id
  role_definition_id = data.azurerm_role_definition.table_data_contrib.id
  scope              = var.storage_account_id
  skip_service_principal_aad_check = true
}







