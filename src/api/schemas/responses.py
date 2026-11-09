"""Pydantic response models for API endpoints."""

from typing import Any

from pydantic import BaseModel


class ModelInfoResponse(BaseModel):
    id: str
    name: str
    provider: str
    enabled: bool
    available: bool
    pricing: dict[str, Any] | None = None
    description: str | None = None


class ModelListResponse(BaseModel):
    models: list[ModelInfoResponse]
    total: int


class GenericSuccessResponse(BaseModel):
    success: bool
    message: str
    data: dict[str, Any] | None = None
