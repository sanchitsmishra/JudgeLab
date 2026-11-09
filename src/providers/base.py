from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class GenerationConfig:
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float | None = None
    extra_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderError:
    type: str
    message: str
    retryable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProviderResponse:
    success: bool
    model: str
    provider: str
    answer: str | None = None
    latency_seconds: float = 0.0
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None
    raw_metadata: dict[str, Any] = field(default_factory=dict)
    error: ProviderError | None = None

    def to_dict(self) -> dict[str, Any]:
        data = {
            "success": self.success,
            "model": self.model,
            "provider": self.provider,
            "answer": self.answer,
            "latency_seconds": round(self.latency_seconds, 3),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost": self.estimated_cost,
            "raw_metadata": self.raw_metadata,
        }
        if self.error:
            data["error"] = self.error.to_dict()
        else:
            data["error"] = None
        return data


class BaseProvider(ABC):
    """Abstract Base Class for all LLM providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the provider (e.g., 'openai', 'anthropic', 'mock')."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is configured and reachable."""
        pass

    @abstractmethod
    async def generate(
        self,
        model_name: str,
        prompt: str,
        system_prompt: str | None = None,
        generation_config: GenerationConfig | None = None,
    ) -> ProviderResponse:
        """Generate response from model and return standardized ProviderResponse."""
        pass
