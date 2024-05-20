terraform {
  required_version = ">= 1.7.2"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.104.0"
    }
  }
}
