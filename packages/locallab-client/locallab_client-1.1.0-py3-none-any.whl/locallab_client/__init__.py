"""
LocalLab Python Client

A Python client for interacting with LocalLab, a local LLM server.
"""

from .client import (
    LocalLabClient,
    LocalLabConfig,
    GenerateOptions,
    ChatMessage,
    GenerateResponse,
    ChatResponse,
    BatchResponse,
    ModelInfo,
    SystemInfo,
    LocalLabError,
    ValidationError,
    RateLimitError,
)
from .sync_client import SyncLocalLabClient

__version__ = "1.0.8"
__author__ = "Utkarsh"
__email__ = "utkarshweb2023@gmail.com"

__all__ = [
    "LocalLabClient",
    "SyncLocalLabClient",
    "LocalLabConfig",
    "GenerateOptions",
    "ChatMessage",
    "GenerateResponse",
    "ChatResponse",
    "BatchResponse",
    "ModelInfo",
    "SystemInfo",
    "LocalLabError",
    "ValidationError",
    "RateLimitError",
]
