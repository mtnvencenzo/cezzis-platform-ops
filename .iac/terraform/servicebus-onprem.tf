module "servicebus_cezzis_onprem_sync_topic" {
  source = "git::ssh://git@github.com/mtnvencenzo/Terraform-Modules.git//modules/servicebus-topic"

  namespace_id        = data.azurerm_servicebus_namespace.servicebus_namespace.id
  name_discriminator  = "cloud-sync"
  sub                 = var.sub
  region              = var.region
  environment         = "prm"
  domain              = var.domain
  resource_group_name = data.azurerm_resource_group.cocktails_resource_group.name
  location            = data.azurerm_resource_group.cocktails_resource_group.location

  providers = {
    azurerm = azurerm
  }

  tags = local.tags
}

resource "azurerm_servicebus_topic_authorization_rule" "cezzis_onprem_cloud_sync_topic_send" {
  name     = "send"
  topic_id = module.servicebus_cezzis_onprem_sync_topic.id
  listen   = false
  send     = true
  manage   = false
}