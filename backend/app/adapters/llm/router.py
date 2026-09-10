"""Model-role router (doc 00 A16): roles are architecture, concrete models
are configuration derived from benchmarks. The router never invents models —
unknown roles/tasks fail loudly."""

import json
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "config" / "model_roles.json"

VALID_ROLES = {
    "FAST_MODEL",
    "DEFAULT_EXTRACTION_MODEL",
    "COMPLEX_EXTRACTION_MODEL",
    "ESCALATION_MODEL",
}


class ModelRouter:
    def __init__(self, config_path: Path | None = None):
        path = config_path or DEFAULT_CONFIG
        config = json.loads(Path(path).read_text())
        self.roles: dict[str, str] = config["roles"]
        self.task_routing: dict[str, str] = config.get("task_routing", {})
        self.cost_controls: dict = config.get("cost_controls", {})
        unknown = set(self.roles) - VALID_ROLES
        if unknown:
            raise ValueError(f"unknown model roles in config: {sorted(unknown)}")

    def resolve_role(self, role: str) -> str:
        if role not in self.roles:
            raise KeyError(f"model role not configured: {role}")
        return self.roles[role]

    def resolve_task(self, task: str) -> tuple[str, str]:
        """→ (role, concrete_model_id) for a named task."""
        if task not in self.task_routing:
            raise KeyError(f"no model routing configured for task: {task}")
        role = self.task_routing[task]
        return role, self.resolve_role(role)

    def escalate(self, role: str) -> tuple[str, str]:
        """Escalation path for low-confidence/difficult cases (A16)."""
        return "ESCALATION_MODEL", self.resolve_role("ESCALATION_MODEL")
