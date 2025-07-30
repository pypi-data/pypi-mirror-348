from typing import Any, ClassVar, Generic, Literal, TypeVar

from pydantic import BaseModel

from moxn_models.blocks.base import BlockType
from moxn_models.blocks.image import ImageContentFromSourceModel
from moxn_models.blocks.text import TextContentModel

T = TypeVar("T")


class ToolCallModel(BaseModel):
    block_type: ClassVar[Literal[BlockType.TOOL_CALL]] = BlockType.TOOL_CALL
    id: str
    arguments: str | dict[str, Any] | None
    name: str


class ToolResultBase(BaseModel, Generic[T]):
    block_type: ClassVar[Literal[BlockType.TOOL_RESULT]] = BlockType.TOOL_RESULT
    type: Literal["tool_use"]
    id: str
    name: str
    content: T | None


class ToolResultModel(
    ToolResultBase[TextContentModel | ImageContentFromSourceModel | None]
):
    type: Literal["tool_use"]
    id: str
    name: str
    content: TextContentModel | ImageContentFromSourceModel | None
