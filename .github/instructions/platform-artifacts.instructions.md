---
name: Platform Artifact Instructions
description: "Use when writing or reviewing observability exports, Draw.io assets, generated SVGs, or model definition files in this repo. Covers preserving exported structure, reducing churn, and keeping operator-facing artifacts aligned with platform behavior."
applyTo: ".observability/**/*.json,.observability/**/*.ndjson,.ai/models/**/*.Modelfile,*.drawio,*.drawio.svg"
---

# Platform Artifact Instructions

- Treat observability exports, Draw.io files, generated SVGs, and model definition files as operational artifacts rather than ordinary hand-written source code.
- Preserve exported or generated structure whenever practical. Avoid unrelated formatting churn.
- Keep dashboards, diagrams, and model assets aligned with the current platform architecture and operator workflow documented in `README.md`.
- When changing a Draw.io diagram, keep the paired exported SVG in sync when the repo uses one.
- When changing a model definition file, preserve the existing invocation comments, base model conventions, and parameter style unless the change explicitly requires a contract update.
