---
name: review-platform-ops-change
description: 'Review Kubernetes, ArgoCD, Terraform, GitHub Actions, and related platform artifact changes in this repo for safety, contract alignment, validation gaps, and deployment-risk regressions. Use when the change already exists and the main task is adversarial review.'
argument-hint: 'Provide the changed platform ops files, or describe the operational behavior being reviewed so the review can focus on correctness and deployment risk.'
user-invocable: true
---

# Review Platform Ops Change

Use this skill when the platform operations change already exists and the main task is to review it like production code.

## What To Review

Review the changed files together with:
- adjacent Kubernetes or ArgoCD manifests when local bootstrap behavior is involved
- adjacent Terraform resources or module calls
- any matching workflow callers under `.github/workflows/`
- observability exports, diagrams, or model assets when operator-facing artifacts changed
- `README.md` when the change affects prerequisites, deployment, or operator workflow

## Required Review Standards

- Treat Kubernetes, ArgoCD, Terraform, workflow, and operator-facing artifact files as production-impacting assets.
- Confirm the change is scoped to the intended infrastructure behavior and does not include unrelated cleanup.
- Confirm namespace conventions, sync-wave ordering, ArgoCD destination settings, and secret-store references still align when local bootstrap files change.
- Confirm naming, tags, providers, and module usage stay consistent with neighboring patterns.
- Confirm workflow triggers, path filters, secrets, variables, and reusable workflow inputs still match the Terraform layer.
- Confirm validation expectations are met, especially `terraform fmt` and practical `terraform validate` coverage.
- Confirm the review does not assume implicit Terraform or cluster mutation execution.

## Common Findings To Look For

- incorrect Kustomize composition, namespace, sync-wave, or secret-store references
- ArgoCD `repoURL`, `path`, `destination.namespace`, or sync policy drift
- incorrect working directory, backend, environment, or state key values
- path filters that fail to trigger or trigger too broadly
- secrets or variables renamed in one place but not the other
- Terraform resource naming or discriminator drift relative to existing patterns
- missing contract updates when ingress, messaging, DNS, storage, or secrets changed
- stale diagrams, dashboards, or README guidance after operator workflow changed
- formatting drift that `terraform fmt` would correct
- risky workflow behavior that could mutate infrastructure on pull requests

## Validation Guidance

- Prefer non-mutating validation such as `terraform fmt -recursive .iac/terraform` and `terraform validate`.
- For Kubernetes or ArgoCD changes, prefer focused manifest and composition review before any execution-level actions.
- For workflow-only changes, review YAML correctness and reusable workflow contract alignment.
- Do not run `terraform apply`, `terraform destroy`, `kubectl apply`, `kubectl delete`, or ArgoCD sync-style commands as part of routine review.

## Expected Output

The review result should:
- list findings first, ordered by severity
- call out workflow, namespace, sync, or state-coordinate issues explicitly
- state whether the platform ops changes appear safe for normal validation or review workflows
- state whether the change should be corrected in place or is acceptable as written

