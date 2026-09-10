"""Vision/LLM provider abstraction (doc 00 A16; doc 06 §2).

Providers do transport only: request in, raw text + usage out. They never
validate science, never assign confidence, and never retry semantically —
that belongs to the calling stage. Every response carries the CONCRETE model
id used (A16) so provenance can record it.
"""

import hashlib
from dataclasses import dataclass, field


@dataclass(frozen=True)
class VisionRequest:
    """One bounded-region interpretation request. `image_png` is the rendered
    figure region only — never a whole PDF (researcher directive, Phase 1b)."""

    prompt: str
    prompt_id: str
    prompt_version: str
    image_png: bytes
    model_id: str
    model_role: str
    max_tokens: int = 4000

    def cache_key(self) -> str:
        h = hashlib.sha256()
        h.update(self.model_id.encode())
        h.update(self.prompt_id.encode())
        h.update(self.prompt_version.encode())
        h.update(hashlib.sha256(self.prompt.encode()).digest())
        h.update(hashlib.sha256(self.image_png).digest())
        return h.hexdigest()


@dataclass
class LLMResponse:
    text: str
    model_id: str            # concrete model that actually answered (A16)
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    est_cost_usd: float | None = None
    raw_meta: dict = field(default_factory=dict)


class ProviderFailure(Exception):
    """Transport-level failure (network, auth, 5xx). Retryable by the stage;
    becomes stage-state API_FAILURE, never a domain fact (§60)."""


class VisionProvider:  # Protocol by convention (kept a base class for fakes)
    provider_name: str = "abstract"

    def interpret_image(self, request: VisionRequest) -> LLMResponse:  # pragma: no cover
        raise NotImplementedError
