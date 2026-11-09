"""Pydantic schemas for API request validation."""

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class GenerationConfigSchema(BaseModel):
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=8192)
    top_p: float | None = Field(default=None, ge=0.0, le=1.0)
    extra_params: dict[str, Any] = Field(default_factory=dict)


class GenerateCompareRequest(BaseModel):
    models: list[str] = Field(
        ..., description="List of 1 to 4 model identifiers (e.g. ['gemini:gemini-1.5-flash'])"
    )
    prompt: str = Field(..., description="Problem statement or prompt to evaluate")
    system_prompt: str | None = Field(default=None, description="Optional system instructions")
    generation_config: GenerationConfigSchema | None = Field(default=None)
    position_swap_check: bool | None = Field(
        default=None, description="Run position swap consistency check"
    )
    custom_api_keys: dict[str, str] | None = Field(
        default=None, description="Optional per-user API keys for providers"
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Prompt cannot be empty.")
        if len(clean) > 200_000:
            raise ValueError("Prompt exceeds maximum length limit of 200,000 characters.")
        return clean

    @field_validator("models")
    @classmethod
    def validate_models(cls, v: list[str]) -> list[str]:
        if len(v) < 1:
            raise ValueError("At least 1 model must be selected.")
        if len(v) > 4:
            raise ValueError(f"At most 4 models can be selected (got {len(v)}).")
        if len(set(v)) != len(v):
            raise ValueError("Duplicate models are not permitted.")
        return v


class ManualAnswerItem(BaseModel):
    model_name: str = Field(..., description="Name or identifier of the candidate model")
    answer: str = Field(..., max_length=200_000, description="Candidate answer text")

    @field_validator("model_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Model name cannot be empty.")
        return clean

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Candidate answer text cannot be empty.")
        return clean


class ManualCompareRequest(BaseModel):
    problem: str = Field(..., max_length=200_000, description="Problem statement or question")
    answers: list[ManualAnswerItem] = Field(..., description="List of 2 to 4 candidate answers")
    position_swap_check: bool | None = Field(
        default=None, description="Run position swap consistency check"
    )

    @field_validator("problem")
    @classmethod
    def validate_problem(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Problem cannot be empty.")
        return clean

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, v: list[ManualAnswerItem]) -> list[ManualAnswerItem]:
        if len(v) < 2:
            raise ValueError(f"At least 2 answers are required (got {len(v)}).")
        if len(v) > 4:
            raise ValueError(f"At most 4 answers can be compared (got {len(v)}).")
        names = [a.model_name for a in v]
        if len(set(names)) != len(names):
            raise ValueError("Model names in candidate answers must be unique.")
        return v


class SaveOptionsSchema(BaseModel):
    prompt: bool = True
    answers: bool = True
    evaluations: bool = True
    metrics: bool = True
    raw_responses: bool = False


class SaveSessionRequest(BaseModel):
    save_options: SaveOptionsSchema = Field(default_factory=SaveOptionsSchema)
    session_data: dict[str, Any] = Field(..., description="Full session report data to persist")


class AsyncEvaluationRequest(BaseModel):
    mode: Literal["GENERATE_AND_COMPARE", "MANUAL_COMPARE"]
    generate: GenerateCompareRequest | None = None
    manual: ManualCompareRequest | None = None

    @model_validator(mode="after")
    def validate_mode_payload(self):
        if self.mode == "GENERATE_AND_COMPARE" and (not self.generate or self.manual):
            raise ValueError("Provide only the generate payload for GENERATE_AND_COMPARE mode.")
        if self.mode == "MANUAL_COMPARE" and (not self.manual or self.generate):
            raise ValueError("Provide only the manual payload for MANUAL_COMPARE mode.")
        return self
