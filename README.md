# Cezzis Platform Ops

This repository is the operations and infrastructure home for the Cezzis platform. It now combines local Kubernetes and ArgoCD deployment setup, production-oriented shared Terraform, observability artifacts, architecture diagrams, and supporting AI model assets for the broader cezzis.com solution.

This repo should be treated as the authoritative operational reference for how the platform is structured and how core shared infrastructure and deployment assets fit together.

## What This Repo Contains

At a high level, this repository owns:

- local Kubernetes bootstrap and shared namespace resources
- ArgoCD application entry points for syncing platform manifests
- production shared Azure infrastructure managed with Terraform
- observability dashboard exports and related artifacts
- architecture diagrams and supporting solution documentation
- AI model assets used for platform-adjacent workflows
- GitHub Actions and Copilot configuration that support safe operations work in this repo

## Architecture Overview

The diagram below is the current high-level view of the cezzis.com platform and its major relationships.

![Cezzis platform architecture](./cezzis-com.drawio.svg)

## Repository Layout

- `.iac/k8s/`: local Kubernetes platform manifests managed through Kustomize
- `.iac/argocd/`: ArgoCD application definitions used to sync platform manifests into the cluster
- `.iac/terraform/`: production-oriented shared Azure infrastructure
- `.iac/terraform/environment_vars/`: environment-specific tfvars values
- `.observability/`: exported dashboards and observability assets
- `.ai/models/`: AI model and prompt artifacts, including Ollama modelfiles
- `.github/workflows/`: CI/CD workflow callers for Terraform validation and deployment
- `.github/`: Copilot instructions, hooks, and skills for working safely in this repo
- `cezzis-com.drawio` and `cezzis-com.drawio.svg`: solution diagrams used as operational references

## Kubernetes And ArgoCD Assets

The local cluster setup currently centers on `.iac/k8s/kustomization.yaml`, which composes shared platform resources such as:

- the `cezzis` namespace
- shared pod data configuration
- parameter secret stores
- Dapr token external secret wiring

ArgoCD bootstraps those manifests through `.iac/argocd/cezzis-platform-ops.yaml`, which points at the `.iac/k8s` path and syncs it into the `cezzis` namespace.

Typical bootstrap flow:

```bash
kubectl apply -f .iac/argocd/cezzis-platform-ops.yaml
kubectl apply -k .iac/k8s
```

If you need to expose Azure Container Registry pull credentials or Azure service principal credentials into the namespace, use the same secret-creation workflow documented by the platform team for the target environment before syncing workloads.

## Shared Terraform For Production

The Terraform configuration under `.iac/terraform` manages the shared Azure layer for the platform. Based on the current files, that includes resources such as:

- Azure Front Door and CDN configuration
- Front Door custom domain wiring
- API Management integration and policies
- DNS records
- Key Vault resources and access policies
- Storage Account resources
- Service Bus namespaces and topics
- supporting shared configuration, providers, locals, and environment values

The current Terraform configuration uses:

- Terraform `1.11.4` in CI
- `hashicorp/azurerm` provider `4.58.0`
- Azure remote state via the `azurerm` backend
- environment-specific values from files such as `.iac/terraform/environment_vars/prd.tfvars`

The naming and tagging model is driven by variables such as `product`, `domain`, `sub`, `region`, `environment`, and `sequence`, with shared tags defined in `.iac/terraform/locals.tf`.

## Local Validation

Prefer non-mutating validation by default.

For Terraform changes:

```bash
terraform fmt -recursive .iac/terraform
cd .iac/terraform
terraform init -backend=false
terraform validate
```

Notes:

- Run `terraform fmt -recursive .iac/terraform` whenever `.tf` files change.
- `terraform init -backend=false` is useful for local validation when you need provider or module initialization without touching remote state.
- Do not run `terraform apply` or `terraform destroy` implicitly as part of routine work.

For Kubernetes manifest changes, prefer targeted review of the Kustomize composition and ArgoCD application definition before applying changes to a live cluster.

## Deployment Workflow

The main Terraform workflow is `.github/workflows/cezzis-shared-infrastructure-cicd.yaml`.

That workflow currently:

- runs for pushes and pull requests affecting `.iac/terraform/**`
- uses a reusable workflow for Terraform plan and apply behavior
- targets the `.iac/terraform` working directory
- uses the `prd` environment name
- configures Azure backend state through workflow inputs, variables, and secrets

Changes to Terraform structure, environment inputs, secrets, or backend coordinates should be reviewed together with the workflow caller to avoid contract drift.

## Observability And Supporting Artifacts

This repo also contains operational artifacts beyond deployment manifests and Terraform:

- `.observability/elastic/`: exported Elastic dashboards
- `.observability/openobserve/`: exported OpenObserve dashboards
- `.ai/models/qwen2.5-coder:32b-instruct-q6_K/Mixology.Modelfile`: an Ollama modelfile used for mixology-oriented AI behavior
- top-level Draw.io assets for platform architecture documentation

These assets are part of the platform’s operational reference set and should stay aligned with the deployed or intended platform behavior.

## Repository Role In The Wider Platform

This repo now serves as the full Cezzis Platform Ops repository rather than a Terraform-only shared infrastructure repo. It sits alongside the application and service repositories and captures the cross-cutting operational layer for the cezzis.com solution.

Use this repository when the change primarily concerns:

- cluster bootstrap or shared Kubernetes resources
- ArgoCD application setup
- shared production Azure infrastructure
- observability exports or operational diagrams
- platform-level deployment or operator documentation

## Change Guidelines

When updating this repository:

- keep changes scoped to the operational surface you are modifying
- preserve existing naming, tagging, module, and manifest patterns before introducing new structures
- review related Azure, Kubernetes, ArgoCD, and workflow surfaces when a change crosses those boundaries
- keep `README.md` aligned with the actual platform layout and operator workflow

## Prerequisites

To work locally, you will typically need:

- Terraform installed
- `kubectl` installed and pointed at the correct cluster when validating Kubernetes assets
- access to Azure appropriate for reading or validating the target configuration
- access to any private Terraform modules referenced by this repo
- GitHub access for reviewing or updating CI workflow behavior
- ArgoCD access when validating application sync behavior

## Troubleshooting

If an ArgoCD application is stuck deleting because of finalizers, a common recovery command is:

```bash
kubectl patch application/<appname> --type json --patch='[{"op":"remove","path":"/metadata/finalizers"}]' -n argocd
```

## License

This project is proprietary software. All rights reserved.
