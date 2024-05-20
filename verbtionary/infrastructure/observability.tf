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

  // These roles appear built-in. Without these, a new action group gets
  // created with these roles.
  //
  // I haven't torn down and stood up the infrastructure to test if having
  // this stops the automatic creation of that action group, but I think
  // there's a good chance...
  arm_role_receiver {
    name                    = "Monitoring Contributor"
    role_id                 = "749f88d5-cbae-40b8-bcfc-e573ddc772fa"
    use_common_alert_schema = true
  }
  arm_role_receiver {
    name                    = "Monitoring Reader"
    role_id                 = "43d0d8ad-25c7-4714-9337-8ba259a9fe05"
    use_common_alert_schema = true
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
