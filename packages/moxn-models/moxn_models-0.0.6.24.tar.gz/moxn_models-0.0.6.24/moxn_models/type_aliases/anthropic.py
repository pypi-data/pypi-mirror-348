"""Type definitions for Anthropic provider-specific content blocks."""

from typing import TYPE_CHECKING, Any, Sequence, TypedDict, Union

if TYPE_CHECKING:
    # -- Anthropic --
    from anthropic.types import (
        Base64ImageSourceParam as AnthropicBase64ImageSourceParam,
    )
    from anthropic.types import (
        Base64PDFSourceParam as AnthropicBase64PDFSourceParam,
    )
    from anthropic.types import (
        DocumentBlockParam as AnthropicDocumentBlockParam,
    )
    from anthropic.types import (
        ImageBlockParam as AnthropicImageBlockParam,
    )
    from anthropic.types import (
        TextBlockParam as AnthropicTextBlockParam,
    )
    from anthropic.types import (
        ToolResultBlockParam as AnthropicToolResultBlockParam,
    )
    from anthropic.types import (
        ToolUseBlockParam as AnthropicToolUseBlockParam,
    )
    from anthropic.types import URLImageSourceParam as AnthropicURLImageSourceParam
    from anthropic.types import (
        URLPDFSourceParam as AnthropicURLPDFSourceParam,
    )
    from anthropic.types.cache_control_ephemeral_param import (
        CacheControlEphemeralParam as AnthropicCacheControlEphemeralParam,
    )
else:
    AnthropicBase64PDFSourceParam = Any
    AnthropicDocumentBlockParam = Any
    AnthropicImageBlockParam = Any
    AnthropicTextBlockParam = Any
    AnthropicToolUseBlockParam = Any
    AnthropicToolResultBlockParam = Any
    AnthropicURLPDFSourceParam = Any
    AnthropicCacheControlEphemeralParam = Any


# Anthropic content block types
AnthropicContentBlock = Union[
    AnthropicTextBlockParam,
    AnthropicImageBlockParam,
    AnthropicDocumentBlockParam,
    AnthropicToolUseBlockParam,
    AnthropicToolResultBlockParam,
]

AnthropicSystemContentBlock = AnthropicTextBlockParam
AnthropicDocumentSourceBlock = (
    AnthropicBase64PDFSourceParam | AnthropicURLPDFSourceParam
)
AnthropicImageSourceBlock = (
    AnthropicBase64ImageSourceParam | AnthropicURLImageSourceParam
)


# Provider-specific block sequences (for grouping operations)
AnthropicContentBlockSequence = Sequence[Sequence[AnthropicContentBlock]]
AnthropicSystemContentBlockSequence = Sequence[Sequence[AnthropicSystemContentBlock]]


class AnthropicMessagesParam(TypedDict, total=False):
    system: str | list[AnthropicSystemContentBlock]
    messages: list[AnthropicContentBlock]
