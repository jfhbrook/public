// Set the secret with clickops
resource "azurerm_key_vault_secret" "merriam_webster_api_key" {
  name         = "MerriamWebsterApiKey"
  value        = "CHANGEME"
  key_vault_id = azurerm_key_vault.verbtionary.id

  lifecycle {
    ignore_changes = [
      value
    ]
  }

  depends_on = [
    azurerm_key_vault_access_policy.client
  ]
}

resource "azurerm_linux_function_app" "verbtionary" {
  name                = coalesce(var.app_name, var.name)
  resource_group_name = azurerm_resource_group.verbtionary.name
  location            = azurerm_resource_group.verbtionary.location

  storage_account_name       = azurerm_storage_account.verbtionary.name
  storage_account_access_key = azurerm_storage_account.verbtionary.primary_access_key
  service_plan_id            = azurerm_service_plan.verbtionary.id

  functions_extension_version = "~4"

  site_config {
    application_stack {
      powershell_core_version = "7"
    }
    application_insights_key = azurerm_application_insights.verbtionary.instrumentation_key
  }

  app_settings = {
    // Managed by azure functions core tools, but defaulted and ignored here.
    "WEBSITE_RUN_FROM_PACKAGE" = 1
    "MERRIAM_WEBSTER_API_KEY"  = "@Microsoft.KeyVault(VaultName=${azurerm_key_vault.verbtionary.name};SecretName=${azurerm_key_vault_secret.merriam_webster_api_key.name})"
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [
      app_settings["WEBSITE_RUN_FROM_PACKAGE"]
    ]
  }
}

resource "azurerm_service_plan" "verbtionary" {
  name                = "${var.name}-service-plan"
  resource_group_name = azurerm_resource_group.verbtionary.name
  location            = azurerm_resource_group.verbtionary.location
  os_type             = "Linux"
  sku_name            = "B1"
}
