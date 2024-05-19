resource "azurerm_resource_group" "verbtionary" {
  name     = var.name
  location = "West US 2"
}

data "azurerm_client_config" "current" {}
