from datetime import datetime
from typing import ClassVar, Literal

from moxn_models.blocks.base import BaseContent, BlockType


class SignedURLContentModel(BaseContent):
    block_type: ClassVar[Literal[BlockType.SIGNED]] = BlockType.SIGNED
    key: str
    expiration: datetime | None = None
    ttl_seconds: int = 3600
    buffer_seconds: int = 300
    signed_url: str | None = None
