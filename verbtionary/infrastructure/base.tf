resource "azurerm_resource_group" "verbtionary" {
  name     = "verbtionary-v2"
  location = "West US 2"
}

data "azurerm_client_config" "current" {}
