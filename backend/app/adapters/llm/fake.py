"""Test/replay providers (doc 06 §7): the pipeline must run offline.

- FakeVisionProvider: scripted responses (per-call or constant), can simulate
  transport failures and malformed output.
- ReplayVisionProvider: serves recorded responses from a fixture directory,
  keyed by request cache_key. Strict: a missing fixture is an error, so tests
  can never silently hit the network.
- RecordingVisionProvider: wraps a real provider and writes fixtures for
  later replay.
"""

import json
from pathlib import Path

from app.adapters.llm.provider import (
    LLMResponse,
    ProviderFailure,
    VisionProvider,
    VisionRequest,
)


class FakeVisionProvider(VisionProvider):
    provider_name = "fake"

    def __init__(self, responses: list[str | Exception] | None = None):
        self.responses = list(responses or [])
        self.calls: list[VisionRequest] = []

    def interpret_image(self, request: VisionRequest) -> LLMResponse:
        self.calls.append(request)
        if not self.responses:
            raise ProviderFailure("fake provider exhausted")
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return LLMResponse(
            text=item,
            model_id=f"fake:{request.model_id}",
            input_tokens=100,
            output_tokens=len(item) // 4,
            latency_ms=1,
            est_cost_usd=0.0,
        )


class ReplayVisionProvider(VisionProvider):
    provider_name = "replay"

    def __init__(self, fixture_dir: Path):
        self.fixture_dir = Path(fixture_dir)

    def interpret_image(self, request: VisionRequest) -> LLMResponse:
        path = self.fixture_dir / f"{request.cache_key()}.json"
        if not path.exists():
            raise ProviderFailure(
                f"no recorded fixture for request {request.cache_key()[:12]}… "
                f"(prompt {request.prompt_id} v{request.prompt_version}, model {request.model_id})"
            )
        data = json.loads(path.read_text())
        return LLMResponse(
            text=data["text"],
            model_id=data.get("model_id", f"replay:{request.model_id}"),
            input_tokens=data.get("input_tokens", 0),
            output_tokens=data.get("output_tokens", 0),
            latency_ms=0,
            est_cost_usd=0.0,
            raw_meta={"replayed": True},
        )


class RecordingVisionProvider(VisionProvider):
    provider_name = "recording"

    def __init__(self, inner: VisionProvider, fixture_dir: Path):
        self.inner = inner
        self.fixture_dir = Path(fixture_dir)
        self.fixture_dir.mkdir(parents=True, exist_ok=True)

    def interpret_image(self, request: VisionRequest) -> LLMResponse:
        response = self.inner.interpret_image(request)
        path = self.fixture_dir / f"{request.cache_key()}.json"
        path.write_text(
            json.dumps(
                {
                    "text": response.text,
                    "model_id": response.model_id,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                },
                indent=2,
            )
        )
        return response
