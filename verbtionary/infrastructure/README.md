# Verbtionary Infrastructure

The infrastructure setup for Verbtionary is structured as a Terraform module.
I use it in a Terraform project in my private files to stand it up.

## Usage

Usage looks something like this:

```hcl
module "verbtionary" {
  source = "git@github.com:jfhbrook/public.git//verbtionary/infrastructure?ref=main"

  name        = "verbtionary"
  alert_email = "..."
}

resource "azurerm_key_vault_access_policy" "josh" {
  key_vault_id = module.verbtionary.key_vault_id
  tenant_id    = "..."
  object_id    = "..."

  key_permissions = [
  ]

  secret_permissions = [
    "Backup",
    "Delete",
    "Get",
    "List",
    "Purge",
    "Recover",
    "Restore",
    "Set",
  ]

  storage_permissions = [
  ]
}
```

Of note here is that I take the ID of the key vault created by the module and
give myself access to it. This is because Terraform creates the key vault and
secret, but expects me to update the secret's value with clickops.

Otherwise, it creates a resource group and a bunch of resources underneath it.
The meat of things is in [app.tf](./app.tf).

## Development

Honestly, I just push to main and run `terraform init -upgrade` in my project.
I know there are better ways, but I'm running pretty casual so it works for
me.
