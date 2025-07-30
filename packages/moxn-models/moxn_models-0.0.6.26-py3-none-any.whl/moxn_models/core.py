from datetime import datetime
from typing import Generic, Sequence, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from moxn_models.blocks.content_block import ContentBlockModel
from moxn_models.content import Author, MessageRole

T = TypeVar("T")


class BaseHeaders(BaseModel):
    user_id: str
    org_id: str | None = None
    api_key: SecretStr

    def to_headers(self) -> dict[str, str]:
        return {
            "user_id": self.user_id,
            "org_id": self.org_id or "",
            "api_key": self.api_key.get_secret_value(),
        }


class MessageBase(BaseModel, Generic[T]):
    id: UUID | None = None
    version_id: UUID | None = Field(None, alias="versionId")
    name: str
    description: str
    author: Author
    role: MessageRole
    blocks: Sequence[Sequence[T]] = Field(repr=False)

    model_config = ConfigDict(populate_by_name=True)


class Message(MessageBase[ContentBlockModel]):
    blocks: Sequence[Sequence[ContentBlockModel]] = Field(repr=False)


class BasePrompt(BaseModel, Generic[T]):
    id: UUID
    version_id: UUID = Field(..., alias="versionId")
    user_id: UUID = Field(..., alias="userId")
    org_id: UUID | None = Field(None, alias="orgId")
    name: str
    description: str
    task_id: UUID = Field(..., alias="taskId")
    created_at: datetime = Field(..., alias="createdAt")
    messages: Sequence[T]
    message_order: Sequence[UUID] = Field(default_factory=list, alias="messageOrder")

    model_config = ConfigDict(populate_by_name=True)


class Prompt(BasePrompt[Message]):
    messages: Sequence[Message]


class BaseTask(BaseModel, Generic[T]):
    id: UUID
    version_id: UUID = Field(..., alias="versionId")
    user_id: UUID = Field(..., alias="userId")
    org_id: UUID | None = Field(None, alias="orgId")
    name: str
    description: str
    created_at: datetime = Field(..., alias="createdAt")
    prompts: Sequence[T]

    model_config = ConfigDict(populate_by_name=True)


class Task(BaseTask[Prompt]):
    prompts: Sequence[Prompt]
