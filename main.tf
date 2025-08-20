locals {
  rg_name            = "iot-gen-ehub"
  sa_data_name       = "sa30906"
  sa_func_name       = "safunc30906"
  table_names        = ["random"]

  eh_namespace_name  = "ehub30906"
  eh_name            = "ehub1"
  eh_tu              = 1
  eh_partitions      = 2
  eh_retention_days  = 1
  eh_consumer_group  = "func"

  iothub_name        = "hub30906"
  eh_endpoint_name   = "eh-endpoint"
  eh_route_name      = "route-to-eh"

  func_name          = "func-ehub30906"
  log_analytics_name = "log-ehub30906"
  appi_name          = "appi-ehub30906"
}

module "rg" {
  source   = "./modules/resource_group"
  name     = local.rg_name
  location = var.location
}

module "sa_data" {
  source              = "./modules/storage"
  account_name        = local.sa_data_name
  resource_group_name = module.rg.name
  location            = module.rg.location
  tables              = local.table_names
}

module "sa_func" {
  source              = "./modules/storage"
  account_name        = local.sa_func_name
  resource_group_name = module.rg.name
  location            = module.rg.location
  tables              = []
}

module "eventhub" {
  source              = "./modules/eventhub"
  resource_group_name = module.rg.name
  location            = module.rg.location

  namespace_name   = local.eh_namespace_name
  eventhub_name    = local.eh_name
  throughput_units = local.eh_tu
  partitions       = local.eh_partitions
  retention_days   = local.eh_retention_days
  consumer_group   = local.eh_consumer_group
}

module "iothub" {
  source              = "./modules/iothub"
  name                = local.iothub_name
  resource_group_name = module.rg.name
  location            = module.rg.location

  endpoint_name             = local.eh_endpoint_name
  route_name                = local.eh_route_name
  eh_send_connection_string = module.eventhub.send_connection_string
  eventhub_connection_string = module.eventhub.send_connection_string
  eventhub_name              = local.eh_name
  depends_on = [module.eventhub]
}

module "function_app" {
  source              = "./modules/function_app"
  name                = local.func_name
  resource_group_name = module.rg.name
  location            = module.rg.location

  runtime_storage_account_name       = module.sa_func.name
  runtime_storage_account_key        = module.sa_func.primary_access_key
  runtime_storage_connection_string  = module.sa_func.primary_connection_string

  eh_listen_connection_string = module.eventhub.listen_connection_string
  eventhub_name               = module.eventhub.eventhub_name
  eh_consumer_group           = module.eventhub.consumer_group

  data_storage_account_id = module.sa_data.id

  log_analytics_name = local.log_analytics_name
  app_insights_name  = local.appi_name

  depends_on = [
    module.iothub,
    module.sa_data,
    module.sa_func,
    module.eventhub
  ]
}
