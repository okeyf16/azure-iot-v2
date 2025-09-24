###################
# Locals for Naming #
#####################
locals {
  resource_group_name       = var.resource_group_name
  location                  = var.location
  iothub_name               = var.iothub_name
  eventhub_namespace_name   = var.eventhub_namespace_name
  eventhub_name             = var.eventhub_name
  storage_account_data_name = var.storage_account_data_name
  storage_account_func_name = var.storage_account_func_name
  table_name                = var.table_name
  function_app_name         = var.function_app_name
  eh_endpoint_name          = var.eh_endpoint_name
  eh_route_name             = var.eh_route_name
  app_insights_name         = "${local.function_app_name}-ai" #new dynamic option
  #app_insights_name        = "fn-iot-ehub-ai"                #previous Static..Please redifine for every deployment if dynamic fails .. 
  tags                      = var.tags
}

######################
# Resource Group     #
######################
module "resource_group" {
  source = "./modules/resource_group"

  name     = local.resource_group_name
  location = local.location
}

######################
# Event Hub          #
######################
module "eventhub" {
  source              = "./modules/eventhub"
  namespace_name      = local.eventhub_namespace_name
  eventhub_name       = local.eventhub_name
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
}

######################
# IoT Hub + Routing  #
######################
module "iothub" {
  source              = "./modules/iothub"
  name                = local.iothub_name
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  tags                = local.tags

  endpoint_name             = local.eh_endpoint_name
  route_name                = local.eh_route_name
  eh_send_connection_string = module.eventhub.send_connection_string
  route_source              = "DeviceMessages"
  route_condition           = "true"

  depends_on = [module.eventhub]
}


###############################
# Storage Account for App Data
###############################
module "sa_data" {
  source               = "./modules/storage"
  account_name         = local.storage_account_data_name
  resource_group_name  = module.resource_group.name
  location             = module.resource_group.location
}

##########################################
# Storage Account for Function Runtime
##########################################
module "sa_func" {
  source               = "./modules/storage"
  account_name         = local.storage_account_func_name
  resource_group_name  = module.resource_group.name
  location             = module.resource_group.location
}

######################
# Log Analytics workspace for function #
######################
module "log_analytics_workspace" {
  source              = "./modules/log_analytics"
  name                = "logs-${local.function_app_name}"
  location            = local.location
  resource_group_name = module.resource_group.name
  tags                = local.tags
}

######################
# Azure Function App #
######################
module "function_app" {
  source                         = "./modules/function_app"
  name                           = local.function_app_name
  resource_group_name            = module.resource_group.name
  location                       = module.resource_group.location
  storage_account_name           = module.sa_func.name
  storage_account_access_key     = module.sa_func.primary_access_key
  eventhub_listen_conn_string    = module.eventhub.listen_connection_string
  eventhub_name                  = local.eventhub_name
  log_analytics_workspace_id     = module.log_analytics_workspace.id
  app_insights_name              = local.app_insights_name
  app_insights_instrumentation_key = module.function_app.app_insights_instrumentation_key
  app_insights_connection_string = module.function_app.app_insights_connection_string
  # table_name                     = local.table_name
  telemetry_table_name           = module.sa_data.telemetry_table_name
  storage_account_id             = module.sa_data.id
  storage_account_data_connection_string = module.sa_data.primary_connection_string
  tags                           = local.tags
  # 👇 Pass IoT Hub connection string here for D2C
  iothub_connection              = module.iothub.connection_string

   # New: pass IoT Hub connection string for C2D
  iothub_service_connection_string = module.iothub.iothub_service_connection_string

  azure_webjobs_storage_connection_string = module.sa_func.primary_connection_string
  
  depends_on = [
    module.iothub,
    module.sa_func,
    module.sa_data,
    module.eventhub,
    module.log_analytics_workspace   # New for dynamic LAW 
  ]
}

######################
# Azure Web App #
######################

module "web_app" {
  source              = "./modules/web_app"
  name                = "iotwebapp309v2"
  plan_name           = "iot-free-plan"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name

  # Connections pulled dynamically
  app_insights_key         = module.function_app.app_insights_instrumentation_key
  app_insights_conn_string = module.function_app.app_insights_connection_string
  storage_conn_str         = module.sa_data.primary_connection_string
  api_key                  = "987654321"

  tags = local.tags
}

