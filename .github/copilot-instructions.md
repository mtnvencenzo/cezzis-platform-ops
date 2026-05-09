# Cezzis Platform Ops Copilot Instructions

## Instruction Precedence

- Treat this file as the source of truth for required repo standards and workflow expectations.
- Treat scoped instruction files under `.github/instructions/` as authoritative for their matching files and domains.
- Treat skills under `.github/skills/` as workflow helpers and reinforcement, not as the only place a required standard is defined.
- If a requirement appears in both a skill and these instructions, follow the stricter interpretation.

## Repository Focus

- This repository is operations-first.
- It contains the shared platform surfaces for cezzis.com, including local Kubernetes and ArgoCD assets, production-oriented Terraform, observability exports, diagrams, and supporting model artifacts.
- GitHub Actions workflow behavior under `.github/workflows/` is part of the deployment contract and should be treated as production-impacting code.
- Changes in this repo often cross operational boundaries. When a change affects Kubernetes, ArgoCD, Terraform, workflows, or operator-facing artifacts together, review the nearest connected surface rather than treating each file in isolation.

## Development Workflow

- Prefer the existing repo workflow and narrow validation over ad hoc broad commands.
- Use `terraform fmt -recursive .iac/terraform` when Terraform files change.
- Use Terraform validation from `.iac/terraform/` when configuration changes are made.
- When Kubernetes or ArgoCD manifests change, review Kustomize composition, namespace expectations, sync-wave annotations, and secret-store references before considering the work complete.
- Treat the reusable GitHub Actions workflow interface as a quality gate for CI changes; keep inputs, secrets, environment names, and backend settings consistent.
- Do not run `terraform apply`, `terraform destroy`, `kubectl apply`, `kubectl delete`, or ArgoCD sync-style commands implicitly as part of normal AI workflow.
- Prefer non-mutating validation such as formatting, `terraform validate`, manifest review, and careful workflow contract checks.
- If deployment execution is explicitly requested, confirm the target environment, cluster, or application and the user intent before proceeding.

## Core Stack

- Kubernetes manifests and Kustomize for local platform bootstrap
- ArgoCD application definitions for cluster synchronization
- Terraform for deployed Azure infrastructure
- GitHub Actions for CI/CD orchestration
- Azure resource composition through shared Terraform modules
- External Secrets, Dapr-related secret wiring, and namespace-scoped operational resources
- Observability dashboard exports for Elastic and OpenObserve
- Diagram and AI model artifacts used as platform support assets

## Project Shape

- Keep local Kubernetes manifests under `.iac/k8s/`.
- Keep ArgoCD application definitions under `.iac/argocd/`.
- Keep production infrastructure under `.iac/terraform/`.
- Keep environment-specific values in `.iac/terraform/environment_vars/`.
- Keep observability exports under `.observability/`.
- Keep model artifacts under `.ai/models/`.
- Keep CI/CD definitions under `.github/workflows/`.
- Treat `README.md` and top-level diagrams as part of the repo contract for setup, validation, architecture, and deployment expectations.

## Infrastructure Standards

- Keep Terraform changes scoped to the target resource or contract change. Avoid unrelated cleanup.
- Preserve existing naming, tagging, backend, and module invocation patterns before introducing new structure.
- Review impacts on dependent Azure surfaces such as Front Door, APIM, DNS, Key Vault, Storage, and Service Bus when changing related Terraform.
- When changing environment variables, secrets, backend configuration, or workflow inputs, verify the corresponding workflow and Terraform expectations still match.
- Prefer extending existing Terraform modules and patterns already used in this repo over introducing one-off resources or inconsistent naming.

## Local Ops Standards

- Keep Kubernetes manifest changes scoped to the intended namespace, secret, config, or bootstrap behavior.
- Preserve the existing `cezzis` namespace conventions, labels, annotations, and ArgoCD-managed expectations before introducing new structure.
- Maintain Kustomize composition deliberately. Add resources in `kustomization.yaml` only when they belong to the local ops bootstrap surface.
- Treat ArgoCD annotations such as sync waves, application path, namespace, and automated sync settings as contract-sensitive configuration.
- When editing secret stores or external secret wiring, verify referenced secret names, namespaces, and Azure Key Vault expectations still line up with the surrounding manifests and Terraform-backed resources.

## Artifact Standards

- Treat exported dashboards, Draw.io files, generated SVGs, and model definition files as operational artifacts rather than general-purpose source code.
- Avoid gratuitous reformatting of exported JSON, NDJSON, or generated SVG content.
- When updating diagrams or observability assets, keep them aligned with the current platform behavior and operator workflow.
- When updating model artifacts, preserve the existing file format and invocation conventions already documented in the file.

## Workflow Standards

- Keep workflow triggers, branch filters, and path filters intentionally narrow.
- Preserve reusable workflow contracts unless the change explicitly requires updating the caller and callee together.
- Treat workflow variables, secrets, backend state coordinates, and deployment guards as production-affecting configuration.
- Avoid introducing commands that mutate infrastructure or clusters automatically on pull requests.
- Keep workflow YAML minimal and explicit; do not add unnecessary steps or duplicate logic already handled by a reusable workflow.

## Validation Standards

- After Terraform changes, run `terraform fmt -recursive .iac/terraform`.
- When practical, run `terraform validate` from `.iac/terraform/` after Terraform changes.
- After Kubernetes or ArgoCD manifest changes, validate the touched slice through focused manifest review, path or namespace checks, Kustomize composition review, and secret or sync ordering alignment.
- After workflow changes, review for YAML validity, trigger correctness, reusable workflow input alignment, and secret or variable name drift.
- Prefer focused validation first, then broader checks only when the change touches multiple operational surfaces.
- Do not treat a diff review alone as sufficient when a narrow executable validation exists.

## Documentation Standards

- Treat `README.md` as part of the repository contract for platform scope, prerequisites, validation steps, architecture, and deployment behavior.
- When changes affect supported resources, workflow behavior, runtime prerequisites, diagrams, observability assets, or operator workflow, review `README.md` for drift and update it when needed.

## Practical Guidance For Copilot

- Before adding a new abstraction, inspect the nearest existing Terraform module usage, Kubernetes manifest, ArgoCD application, or workflow pattern and follow it.
- Prefer small, local changes over broad reshaping of operational assets.
- When changing public ingress, messaging, secrets, DNS, namespace bootstrap, or secret-store behavior, review neighboring files for contract alignment.
- When changing workflow behavior, inspect the referenced reusable workflow call surface before editing the caller.
- When touching exported artifacts, prefer preserving the surrounding structure rather than normalizing everything to a prettier style.
- Prefer ASCII-only edits unless an existing file already requires Unicode.
- Keep comments sparse and only add them when they clarify non-obvious intent.

