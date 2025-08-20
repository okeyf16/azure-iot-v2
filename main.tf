
#####################
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
  namespace_name            = local.eventhub_namespace_name
  eventhub_name             = local.eventhub_name
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
# Azure Function App #
######################
module "function_app" {
  source                         = "./modules/function_app"
  name                           = local.function_app_name
  resource_group_name            = module.resource_group.name
  location                       = module.resource_group.location

  # Runtime
  storage_account_name           = module.sa_func.name
  storage_account_access_key     = module.sa_func.primary_access_key

  # Event Hub trigger
  eventhub_listen_conn_string    = module.eventhub.listen_connection_string
  eventhub_name                  = local.eventhub_name

  # Output destination (Table Storage)
  table_name                     = local.table_name
  storage_account_id             = module.sa_data.id

  tags = local.tags

  depends_on = [
    module.iothub,
    module.sa_func,
    module.sa_data,
    module.eventhub
  ]
}
