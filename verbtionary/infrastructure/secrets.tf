resource "azurerm_key_vault" "verbtionary" {
  name                        = coalesce(var.key_vault_name, "${var.name}keyvault")
  location                    = azurerm_resource_group.verbtionary.location
  resource_group_name         = azurerm_resource_group.verbtionary.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}

resource "azurerm_key_vault_access_policy" "client" {
  key_vault_id = azurerm_key_vault.verbtionary.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  key_permissions = [
  ]

  secret_permissions = [
    "Delete",
    // "Get",
    "List",
    "Purge",
    "Set",
  ]

  storage_permissions = [
  ]
}

resource "azurerm_key_vault_access_policy" "verbtionary" {
  key_vault_id = azurerm_key_vault.verbtionary.id
  tenant_id    = azurerm_linux_function_app.verbtionary.identity[0].tenant_id
  object_id    = azurerm_linux_function_app.verbtionary.identity[0].principal_id

  key_permissions = [
    "Get",
  ]

  secret_permissions = [
    "Get",
  ]

  storage_permissions = [
    "Get",
  ]
}
