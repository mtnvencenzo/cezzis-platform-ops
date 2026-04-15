module "apim_cezzis_antiforgery_jwtsignature_policy" {
  source = "git::ssh://git@github.com/mtnvencenzo/Terraform-Modules.git//modules/apim-jwtsignature-policy-fragment"
  providers = {
    azurerm = azurerm
  }
  environment                     = var.environment
  domain                          = "cezzis"
  name_discriminator              = "api"
  issuers                         = [var.antiforgery_token_issuer]
  keyvault_signaturekey_secret_id = "https://${module.aca_cocktails_api.name}.vault.azure.net/secrets/antiforgery-signing-secret"

  apim_instance = {
    id                  = data.azurerm_api_management.shared_apim.id
    name                = data.azurerm_api_management.shared_apim.name
    resource_group_name = data.azurerm_api_management.shared_apim.resource_group_name
  }

  depends_on = [module.aca_cocktails_api]
}