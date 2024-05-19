resource "azurerm_storage_account" "verbtionary" {
  name                     = coalesce(var.storage_account_name, "${var.name}storage")
  resource_group_name      = azurerm_resource_group.verbtionary.name
  location                 = azurerm_resource_group.verbtionary.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
