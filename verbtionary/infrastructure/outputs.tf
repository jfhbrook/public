output "app_name" {
  value = azurerm_linux_function_app.verbtionary.name
}

output "key_vault_id" {
  value = azurerm_key_vault.verbtionary.id
}

output "default_hostname" {
  value = azurerm_linux_function_app.verbtionary.default_hostname
}
