---
name: GitHub Workflow Instructions
description: "Use when writing or reviewing GitHub Actions workflows in this repo. Covers reusable workflow contracts, trigger safety, secret handling, and Terraform caller alignment."
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml"
---

# GitHub Workflow Instructions

- Workflow files in this repo primarily orchestrate Terraform validation and deployment through reusable workflows.
- Keep branch filters and path filters intentionally narrow so automation only runs for the relevant platform surface.
- Preserve the reusable workflow contract unless the change explicitly updates both the caller and the reusable workflow expectations.
- Treat workflow variables, secrets, backend state coordinates, and deployment guards as production-affecting configuration.
- Avoid adding workflow steps that implicitly apply or destroy infrastructure, mutate a cluster, or bypass existing deployment guards on pull requests.
- When Terraform paths, environment names, backend inputs, or future Kubernetes or ArgoCD paths change, verify the caller still points at the correct target surface and state coordinates.
- Prefer small, explicit workflow edits over broad rewrites.

