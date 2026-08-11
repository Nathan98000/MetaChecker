"""Automated secret-leak guard (researcher directive, Phase 1b live-call
preconditions): no key material in git-tracked files, fixtures, logs, or
error paths; .env excluded from version control."""

import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
KEY_PATTERN = re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}")


def test_no_api_key_material_in_tracked_files():
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    offenders = []
    for rel in tracked:
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        if KEY_PATTERN.search(text):
            offenders.append(rel)
    assert not offenders, f"API-key-like material in tracked files: {offenders}"


def test_env_files_are_gitignored():
    gitignore = (ROOT / ".gitignore").read_text()
    for pattern in (".env", "backend/.env"):
        assert pattern in gitignore, f"{pattern} missing from .gitignore"
    # and git actually ignores a hypothetical backend/.env
    result = subprocess.run(
        ["git", "check-ignore", "backend/.env"], cwd=ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, "git does not ignore backend/.env"


def test_recorded_fixtures_never_contain_key(tmp_path, monkeypatch):
    """Even with a key present in the environment, recorded replay fixtures
    contain only response text/usage — never the key."""
    # sentinel assembled at runtime so the scan test never matches this file
    sentinel = "sk-" + "ant-" + "test-SENTINEL-do-not-leak"
    monkeypatch.setenv("ANTHROPIC_API_KEY", sentinel)
    from app.adapters.llm.fake import FakeVisionProvider, RecordingVisionProvider
    from app.adapters.llm.provider import VisionRequest

    provider = RecordingVisionProvider(
        FakeVisionProvider(['{"rows": []}']), tmp_path
    )
    request = VisionRequest(
        prompt="p", prompt_id="t", prompt_version="1",
        image_png=b"png", model_id="m", model_role="r",
    )
    provider.interpret_image(request)
    fixtures = list(tmp_path.glob("*.json"))
    assert fixtures
    for fixture in fixtures:
        assert "SENTINEL" not in fixture.read_text()


def test_provider_failure_without_key_names_no_secret(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from app.adapters.llm.anthropic_provider import AnthropicVisionProvider
    from app.adapters.llm.provider import ProviderFailure

    with pytest.raises(ProviderFailure) as err:
        AnthropicVisionProvider()
    assert "sk-ant" not in str(err.value)


def test_external_call_log_schema_has_no_secret_column():
    from app.db.models import ExternalCallLog

    columns = {c.name for c in ExternalCallLog.__table__.columns}
    assert not columns & {"api_key", "authorization", "secret", "token"}


def test_frontend_never_references_key():
    frontend = ROOT / "frontend"
    offenders = []
    for path in frontend.rglob("*.ts*"):
        if "node_modules" in path.parts:
            continue
        if "ANTHROPIC_API_KEY" in path.read_text(errors="ignore"):
            offenders.append(str(path))
    assert not offenders, f"frontend references the API key: {offenders}"
