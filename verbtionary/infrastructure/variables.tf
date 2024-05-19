variable "name" {
  type        = string
  description = "The base name for all resources."
}

variable "app_name" {
  type        = string
  description = "The name for the application - this is also the subdomain."
  default     = null
}

variable "storage_account_name" {
  type        = string
  description = "The name of the storage account."
  default     = null
}

variable "key_vault_name" {
  type        = string
  description = "The name of the key vault."
  default     = null
}

variable "alert_email" {
  type        = string
  description = "The email address to send alerts to."
}
