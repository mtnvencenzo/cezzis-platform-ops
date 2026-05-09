---
name: Kubernetes And ArgoCD Instructions
description: "Use when writing or reviewing Kubernetes manifests or ArgoCD application files in this repo. Covers Kustomize composition, namespace conventions, sync-wave ordering, and secret-store or destination alignment."
applyTo: ".iac/k8s/**/*.yml,.iac/k8s/**/*.yaml,.iac/argocd/**/*.yml,.iac/argocd/**/*.yaml"
---

# Kubernetes And ArgoCD Instructions

- Local platform bootstrap assets live under `.iac/k8s/` and `.iac/argocd/`.
- Keep manifest changes scoped to the intended namespace, secret, config, or application-sync behavior.
- Preserve the existing `cezzis` namespace, labels, annotations, and ArgoCD-managed conventions unless the change explicitly requires updating them.
- When editing `.iac/k8s/kustomization.yaml`, keep resources intentionally ordered and limited to the bootstrap surface this repo owns.
- When editing ArgoCD annotations or application files, review `repoURL`, `path`, `destination.namespace`, sync policy, and sync-wave behavior together.
- When editing secret stores or external secret wiring, verify referenced secret names, namespaces, and Azure Key Vault expectations still align with the surrounding manifests and related Terraform-backed resources.
- Avoid applying or deleting manifests implicitly as part of routine AI workflow.
