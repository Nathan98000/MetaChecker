"""Anthropic vision provider. Transport only — no science, no confidence.

Live calls require ANTHROPIC_API_KEY in the environment. Token pricing is
config data (per-model USD per million tokens) so cost estimates stay
auditable; unknown models get no estimate rather than a fabricated one.
"""

import base64
import os
import time
from pathlib import Path

from app.adapters.llm.provider import (
    LLMResponse,
    ProviderFailure,
    VisionProvider,
    VisionRequest,
)


def _key_from_env_file() -> str | None:
    """Fallback: read ANTHROPIC_API_KEY from backend/.env (gitignored — the
    sanctioned local-secret mechanism). The value is returned to the SDK only;
    it is never logged, stored, or included in errors."""
    env_path = Path(__file__).resolve().parents[3] / ".env"
    if not env_path.exists():
        return None
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("ANTHROPIC_API_KEY=") and not line.startswith("#"):
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            return value or None
    return None

# USD per million tokens (input, output); config data, update with pricing.
PRICING: dict[str, tuple[float, float]] = {
    "claude-fable-5": (5.00, 25.00),
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-haiku-4-5-20251001": (1.00, 5.00),
}


class AnthropicVisionProvider(VisionProvider):
    provider_name = "anthropic"

    def __init__(self, api_key: str | None = None):
        self._api_key = (
            api_key or os.environ.get("ANTHROPIC_API_KEY") or _key_from_env_file()
        )
        if not self._api_key:
            raise ProviderFailure(
                "ANTHROPIC_API_KEY is not configured (checked environment and "
                "backend/.env); live vision extraction is unavailable "
                "(use the replay provider for offline runs)."
            )
        import anthropic

        # SDK-level exponential-backoff retries absorb transient 429/529s;
        # anything that still escapes becomes a ProviderFailure and rides the
        # job queue's own at-least-once retry.
        self._client = anthropic.Anthropic(api_key=self._api_key, max_retries=5)

    def interpret_image(self, request: VisionRequest) -> LLMResponse:
        start = time.perf_counter()
        try:
            message = self._client.messages.create(
                model=request.model_id,
                max_tokens=request.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64.b64encode(request.image_png).decode(),
                                },
                            },
                            {"type": "text", "text": request.prompt},
                        ],
                    }
                ],
            )
        except Exception as exc:  # SDK/transport errors → retryable failure
            raise ProviderFailure(f"anthropic call failed: {exc}") from exc

        latency_ms = int((time.perf_counter() - start) * 1000)
        text = "".join(b.text for b in message.content if b.type == "text")
        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        est = None
        if message.model in PRICING or request.model_id in PRICING:
            p_in, p_out = PRICING.get(message.model) or PRICING[request.model_id]
            est = input_tokens / 1e6 * p_in + output_tokens / 1e6 * p_out
        return LLMResponse(
            text=text,
            model_id=message.model,  # concrete versioned id (A16)
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            est_cost_usd=est,
        )
