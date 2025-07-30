"""Type definitions for provider-specific content blocks."""

from typing import TYPE_CHECKING, Any, Sequence, TypedDict, Union

if TYPE_CHECKING:
    # -- Anthropic --
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
else:
    AnthropicDocumentBlockParam = Any
    AnthropicImageBlockParam = Any
    AnthropicTextBlockParam = Any
    AnthropicToolUseBlockParam = Any
    AnthropicToolResultBlockParam = Any

if TYPE_CHECKING:
    # -- Google --
    from google.genai.types import Content as GoogleContent
    from google.genai.types import File as GoogleFile
    from google.genai.types import FunctionCall as GoogleFunctionCall
    from google.genai.types import FunctionResponse as GoogleFunctionResponse
    from google.genai.types import Part as GooglePart


else:
    GoogleContent = Any
    GoogleFile = Any
    GoogleFunctionCall = Any
    GoogleFunctionResponse = Any
    GooglePart = Any

if TYPE_CHECKING:
    # -- OpenAIChat --
    from openai.types.chat import (
        ChatCompletionMessageToolCallParam as OpenAIChatToolUseBlockParam,
    )
    from openai.types.chat.chat_completion_content_part_param import (
        ChatCompletionContentPartParam as OpenAIChatCompletionContentPartParam,
    )
    from openai.types.chat.chat_completion_tool_message_param import (
        ChatCompletionToolMessageParam as OpenAIChatToolResponseParam,
    )
else:
    OpenAIChatToolUseBlockParam = Any
    OpenAIChatToolResponseParam = Any
    OpenAIChatCompletionContentPartParam = Any


# Anthropic content block types
AnthropicContentBlock = Union[
    AnthropicTextBlockParam,
    AnthropicImageBlockParam,
    AnthropicDocumentBlockParam,
    AnthropicToolUseBlockParam,
    AnthropicToolResultBlockParam,
]

AnthropicSystemContentBlock = AnthropicTextBlockParam

# OpenAI content block types
OpenAIChatContentBlock = Union[
    OpenAIChatCompletionContentPartParam,
    OpenAIChatToolUseBlockParam,
    OpenAIChatToolResponseParam,
]

# Google content block types
GoogleContentBlock = Union[
    GoogleContent,
    GoogleFile,
    GoogleFunctionCall,
    GoogleFunctionResponse,
]

GoogleSystemContentBlock = Union[
    GooglePart,
    GoogleFile,
]

# Provider-specific block sequences (for grouping operations)
AnthropicContentBlockSequence = Sequence[Sequence[AnthropicContentBlock]]
AnthropicSystemContentBlockSequence = Sequence[Sequence[AnthropicSystemContentBlock]]
OpenAIChatContentBlockSequence = Sequence[Sequence[OpenAIChatContentBlock]]
GoogleContentBlockSequence = Sequence[Sequence[GoogleContentBlock]]
GoogleSystemContentBlockSequence = Sequence[Sequence[GoogleSystemContentBlock]]

# Generic provider block type (used for functions that work across providers)
ProviderContentBlock = Union[
    AnthropicContentBlock, OpenAIChatContentBlock, GoogleContentBlock
]
ProviderContentBlockSequence = Sequence[Sequence[ProviderContentBlock]]


class GoogleMessagesParam(TypedDict, total=False):
    system_instruction: str
    content: Sequence[GoogleContent | GoogleFile]
