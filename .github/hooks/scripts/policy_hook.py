#!/usr/bin/env python3
import json
import re
import sys
from typing import Any


def deep_find(value: Any, target_keys: set[str], found: list[Any]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in target_keys:
                found.append(item)
            deep_find(item, target_keys, found)
    elif isinstance(value, list):
        for item in value:
            deep_find(item, target_keys, found)


def json_out(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload))


raw = sys.stdin.read()

try:
    data = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    data = {}

event_candidates: list[Any] = []
deep_find(data, {"hookEventName", "eventName"}, event_candidates)
event_name = next((str(item) for item in event_candidates if item), "")

tool_candidates: list[Any] = []
deep_find(data, {"toolName", "tool_name", "recipient_name"}, tool_candidates)
tool_name = next((str(item) for item in tool_candidates if item), "")

command_candidates: list[Any] = []
deep_find(data, {"command"}, command_candidates)
commands = [str(item) for item in command_candidates if isinstance(item, str)]
combined_commands = "\n".join(commands)

path_candidates: list[Any] = []
deep_find(data, {"filePath", "path", "filePaths"}, path_candidates)
paths_text = raw + "\n" + "\n".join(str(item) for item in path_candidates)


def pretool_response(reason: str) -> None:
    json_out(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
            }
        }
    )


if event_name == "PreToolUse":
    terraform_execution = re.search(
        r"(^|\s)terraform\s+(apply|destroy|import|state\s+rm|force-unlock)($|\s)",
        combined_commands,
        re.IGNORECASE,
    )
    kubectl_execution = re.search(
        r"(^|\s)kubectl\s+(apply|delete|patch|replace|rollout\s+restart|scale)($|\s)",
        combined_commands,
        re.IGNORECASE,
    )
    argocd_execution = re.search(
        r"(^|\s)argocd\s+app\s+(sync|delete|create|set)($|\s)",
        combined_commands,
        re.IGNORECASE,
    )
    workflow_dispatch = re.search(
        r"(^|\s)gh\s+workflow\s+run($|\s)",
        combined_commands,
        re.IGNORECASE,
    )

    if terraform_execution:
        pretool_response(
            "Terraform apply-style commands change deployed infrastructure or state. Confirm the target environment and user intent before proceeding."
        )
        sys.exit(0)

    if kubectl_execution:
        pretool_response(
            "kubectl mutation commands can change a live cluster. Confirm the target cluster, namespace, and user intent before proceeding."
        )
        sys.exit(0)

    if argocd_execution:
        pretool_response(
            "ArgoCD app mutation commands can change live sync behavior. Confirm the target application, cluster, and user intent before proceeding."
        )
        sys.exit(0)

    if workflow_dispatch:
        pretool_response(
            "Manual workflow dispatch can trigger deployment behavior. Confirm the intended workflow and target before proceeding."
        )
        sys.exit(0)

if event_name == "PostToolUse":
    terraform_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"\.iac/terraform/.*\.tf|\.tfvars\b",
        paths_text,
        re.IGNORECASE,
    )
    workflow_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"\.github/workflows/.*\.(yml|yaml)\b",
        paths_text,
        re.IGNORECASE,
    )
    k8s_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"\.iac/k8s/.*\.(yml|yaml)\b|\.iac/argocd/.*\.(yml|yaml)\b",
        paths_text,
        re.IGNORECASE,
    )
    artifact_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"\.observability/.*\.(json|ndjson)\b|\.ai/models/.*Modelfile\b|\.drawio(\.svg)?\b",
        paths_text,
        re.IGNORECASE,
    )
    readme_touched = tool_name in {"functions.apply_patch", "functions.create_file"} and re.search(
        r"README\.md\b",
        paths_text,
        re.IGNORECASE,
    )

    messages: list[str] = []
    if terraform_touched:
        messages.append(
            "Terraform files changed. Before finishing, account for `terraform fmt -recursive .iac/terraform` and, when practical, `terraform validate` from `.iac/terraform/`. Also review workflow/backend alignment if environment or state settings changed."
        )
    if workflow_touched:
        messages.append(
            "Workflow files changed. Review trigger filters, reusable workflow inputs, secrets, variables, working directory, and deployment guards before finishing."
        )
    if k8s_touched:
        messages.append(
            "Kubernetes or ArgoCD files changed. Review Kustomize composition, namespace and secret references, sync-wave ordering, application path, and destination alignment before finishing."
        )
    if artifact_touched:
        messages.append(
            "Platform artifact files changed. Preserve exported or generated structure where practical, and review README or diagram/dashboard alignment if operator-facing behavior changed."
        )
    if terraform_touched and not readme_touched:
        messages.append(
            "If the infrastructure change affects prerequisites, supported resources, or operator workflow, review `README.md` for drift before finishing."
        )
    if (k8s_touched or artifact_touched) and not readme_touched:
        messages.append(
            "If the platform ops change affects bootstrap, observability, architecture, or operator workflow, review `README.md` for drift before finishing."
        )

    if messages:
        json_out({"systemMessage": "\n".join(messages)})
        sys.exit(0)

json_out({})
