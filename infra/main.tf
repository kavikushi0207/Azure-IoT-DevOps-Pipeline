terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "iot-factory-rg"
  location = "francecentral"
}

resource "random_id" "hub_id" {
  byte_length = 4
}

resource "azurerm_iothub" "iothub" {
  name                = "factory-hub-${random_id.hub_id.hex}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  sku {
    name     = "F1"
    capacity = "1"
  }
}

output "iot_hub_name" {
  value = azurerm_iothub.iothub.name
}