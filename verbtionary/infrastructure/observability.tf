resource "azurerm_log_analytics_workspace" "verbtionary" {
  name                = "${var.name}-workspace"
  resource_group_name = azurerm_resource_group.verbtionary.name
  location            = azurerm_resource_group.verbtionary.location
  sku                 = "PerGB2018"
}

resource "azurerm_application_insights" "verbtionary" {
  name                = "${var.name}-app-insights"
  resource_group_name = azurerm_resource_group.verbtionary.name
  location            = azurerm_resource_group.verbtionary.location
  workspace_id        = azurerm_log_analytics_workspace.verbtionary.id
  application_type    = "web"
}

resource "azurerm_monitor_action_group" "verbtionary" {
  name                = "${var.name}-failure-emails"
  resource_group_name = azurerm_resource_group.verbtionary.name
  short_name          = "f-email"

  email_receiver {
    name          = "failure-emails"
    email_address = var.alert_email
  }
}

resource "azurerm_monitor_smart_detector_alert_rule" "failure" {
  name                = "${var.name}-failure-alert"
  resource_group_name = azurerm_resource_group.verbtionary.name
  severity            = "Sev3"
  scope_resource_ids = [
    azurerm_application_insights.verbtionary.id
  ]
  frequency     = "PT1M"
  detector_type = "FailureAnomaliesDetector"
  action_group {
    ids = [azurerm_monitor_action_group.verbtionary.id]
  }
}
