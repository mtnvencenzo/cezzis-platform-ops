---
name: add-platform-ops-change
description: 'Add or update platform operations assets in this repo using the existing Kubernetes, ArgoCD, Terraform, GitHub Actions, observability, and documentation patterns. Use for cluster bootstrap changes, shared Azure resource changes, workflow updates, exported artifact updates, and related README drift checks.'
argument-hint: 'Describe the platform ops change, the affected surface such as Kubernetes, ArgoCD, Terraform, workflows, observability, or diagrams, and whether README or operator workflow updates are expected.'
user-invocable: true
---

# Add Platform Ops Change

Use this skill when implementing an operations change in this repository.

This skill is for changes that span one or more of the following:
- Kubernetes updates under `.iac/k8s/`
- ArgoCD application updates under `.iac/argocd/`
- Terraform updates under `.iac/terraform/`
- environment-specific values under `.iac/terraform/environment_vars/`
- GitHub Actions workflow caller updates under `.github/workflows/`
- observability assets under `.observability/`
- model or diagram assets under `.ai/models/` or the repo root
- repository documentation updates in `README.md`

## When To Use

Use this skill for:
- adding or updating shared local cluster bootstrap assets
- changing an existing ArgoCD application definition
- adding or updating a shared Azure resource
- changing an existing Terraform module invocation
- changing backend, variable, or environment expectations
- updating the CI or deployment workflow that validates or deploys Terraform
- updating observability exports, diagrams, or other operator-facing platform artifacts
- implementing a change that affects operator workflow or documented prerequisites

## Repository-Specific Rules

- Keep Kubernetes and ArgoCD bootstrap changes under `.iac/k8s/` and `.iac/argocd/`.
- Keep production infrastructure changes under `.iac/terraform/`.
- Reuse the existing module, naming, tagging, and variable patterns before introducing new structures.
- Prefer non-mutating validation such as `terraform fmt -recursive .iac/terraform` and `terraform validate`.
- Do not run `terraform apply`, `terraform destroy`, `kubectl apply`, `kubectl delete`, or ArgoCD sync-style commands by default.
- Treat workflow YAML as part of the production contract when it controls deployment permissions, state coordinates, or environment gates.
- When public ingress, messaging, secrets, namespace bootstrap, or backend state behavior changes, review neighboring manifests, Terraform, and workflow files for contract alignment.
- Review `README.md` for drift when the change affects prerequisites, validation, deployment, or supported infrastructure.

## Delivery Procedure

### 1. Anchor On The Nearest Existing Pattern

Start from the nearest existing resource, manifest, export, or workflow that matches the requested change.

Good anchors in this repo include:
- the Kustomize composition and neighboring namespace or secret-store manifests in `.iac/k8s/`
- the ArgoCD application file under `.iac/argocd/`
- Service Bus module usage for messaging resources
- Front Door and APIM files for ingress and API-facing configuration
- Key Vault and storage files for secret or storage-related changes
- the existing CI workflow caller under `.github/workflows/` for deployment behavior
- neighboring observability exports or diagrams when the change is artifact-oriented

Do not invent a new repo structure if an adjacent pattern already exists.

### 2. Decide The Minimal Slice

Identify whether the change needs:
- a Kubernetes manifest update
- an ArgoCD application update
- a Terraform-only update
- an environment tfvars update
- a workflow caller update
- an observability, diagram, or model artifact update
- a README update

Prefer the smallest slice that fully implements the change.

### 3. Implement In Repo Order

For a typical infrastructure change, apply changes in this order:

1. Kubernetes or ArgoCD manifests when the bootstrap surface changes
2. Terraform resources, modules, locals, variables, or outputs when shared infrastructure changes
3. environment-specific tfvars if needed
4. workflow caller updates if deployment or validation inputs changed
5. observability, model, or diagram artifacts when operator-facing support assets changed
6. `README.md` updates when prerequisites or operator workflow changed

### 4. Kubernetes And ArgoCD Expectations

When editing Kubernetes or ArgoCD assets:
- preserve the `cezzis` namespace conventions, labels, and annotations
- keep Kustomize composition intentional and limited to the bootstrap assets this repo owns
- verify sync-wave annotations, repo path, destination namespace, and sync policy together
- keep secret-store references, namespaces, and Azure Key Vault expectations aligned with the surrounding manifests

### 5. Terraform Expectations

When editing Terraform:
- keep resource naming and discriminators consistent with neighboring files
- preserve tagging and provider usage patterns
- keep module inputs explicit and aligned with existing conventions
- avoid unrelated formatting or organization changes beyond what `terraform fmt` requires

### 6. Workflow Expectations

When editing workflows:
- keep triggers narrow and intentional
- preserve reusable workflow input names unless coordinated changes are required
- verify backend and environment values still match the Terraform layer
- avoid introducing infrastructure mutation on pull request events

### 7. Artifact Expectations

When editing observability exports, diagrams, or model assets:
- preserve exported or generated structure whenever practical
- avoid gratuitous formatting churn in JSON, NDJSON, or generated SVG output
- keep architecture and operator-facing artifacts aligned with the current platform behavior

### 8. Validation

Prefer the narrowest useful validation first.

Use:
- focused manifest review for `.iac/k8s/` and `.iac/argocd/` changes
- `terraform fmt -recursive .iac/terraform` after `.tf` changes
- `terraform validate` from `.iac/terraform/` when practical
- focused workflow review for YAML correctness, trigger logic, and input or secret alignment after workflow edits

## Review Checklist

Before finishing, verify:
- the change matches an existing repo pattern instead of inventing a new one
- Kubernetes and ArgoCD assets remain scoped to the intended bootstrap or sync behavior
- Terraform remains scoped to the intended Azure contract change
- workflow caller inputs still align with Terraform directory, backend, and environment expectations
- `README.md` was reviewed for drift when prerequisites, validation, or deployment behavior changed
- validation stayed non-mutating unless the user explicitly asked for execution

