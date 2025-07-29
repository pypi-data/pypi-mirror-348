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
    TOOL = "tool"
    MODEL = "model"


class Provider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE_GEMINI = "google_gemini"
    GOOGLE_VERTEX = "google_vertex"


class Author(Enum):
    HUMAN = "human"
    MACHINE = "machine"


class SignedURLContentRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    key: str
    ttl_seconds: int = 3600


class SignedURLContentResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    signed_url: str
    expiration: datetime
    message: str = "Signed URL generated successfully"
