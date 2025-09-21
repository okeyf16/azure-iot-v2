output "url" {
  description = "Web App default hostname"
  value       = azurerm_app_service.this.default_site_hostname
}

output "app_id" {
  description = "Web App ID"
  value       = azurerm_app_service.this.id
}
