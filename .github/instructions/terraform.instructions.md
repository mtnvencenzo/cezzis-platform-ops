---
name: Terraform Instructions
description: "Use when writing or reviewing Terraform in .iac/terraform for this repo. Covers formatting, safe validation, Azure contract awareness, and change-scoping expectations."
applyTo: ".iac/terraform/**/*.tf"
---

# Terraform Instructions

- Production infrastructure for this repo lives under `.iac/terraform/`.
- Keep Terraform changes aligned with the deployed Azure contract, especially Front Door, APIM, DNS, Key Vault, Storage, and Service Bus resources.
- Reuse the existing module invocation and naming patterns before introducing a new structure.
- Keep Terraform changes scoped to the intended resource or contract change. Avoid unrelated cleanup and broad reformatting.
- Terraform formatting matters here. Run `terraform fmt -recursive .iac/terraform` when `.tf` files change.
- When practical, validate from `.iac/terraform/` with `terraform validate` after Terraform edits.
- Be cautious with infrastructure-changing commands such as `terraform apply` or `terraform destroy`; they should not run implicitly.
- When environment values, secrets, backend settings, or shared operational expectations change, review the matching workflow caller and any related Kubernetes or ArgoCD manifests for drift.

