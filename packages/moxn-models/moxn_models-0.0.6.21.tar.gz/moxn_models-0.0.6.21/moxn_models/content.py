from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    SCHEMA = "schema"
    DEVELOPER = "developer"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    MODEL = "model"


class Provider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE_GEMINI = "google_gemini"
    GOOGLE_VERTEX = "google_vertex"


class Author(Enum):
    HUMAN = "human"
    MACHINE = "machine"


def map_role_to_provider(role: MessageRole, provider: Provider) -> MessageRole:
    """
    Maps a MessageRole to the appropriate role for a specific provider.

    Args:
        role: The original MessageRole
        provider: The target provider

    Returns:
        The appropriate MessageRole for the specified provider
    """
    if provider == Provider.OPENAI:
        if role == MessageRole.MODEL:
            return MessageRole.ASSISTANT
        return role
    elif provider == Provider.ANTHROPIC:
        if role == MessageRole.DEVELOPER:
            return MessageRole.SYSTEM
        elif role == MessageRole.MODEL:
            return MessageRole.ASSISTANT
        return role
    elif provider in (Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX):
        if role == MessageRole.ASSISTANT:
            return MessageRole.MODEL
        elif role == MessageRole.DEVELOPER:
            return MessageRole.SYSTEM
        return role
    else:
        raise ValueError(f"Unsupported provider: {provider}")


class SignedURLContentRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    key: str
    ttl_seconds: int = 3600


class SignedURLContentResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    signed_url: str
    expiration: datetime
    message: str = "Signed URL generated successfully"
