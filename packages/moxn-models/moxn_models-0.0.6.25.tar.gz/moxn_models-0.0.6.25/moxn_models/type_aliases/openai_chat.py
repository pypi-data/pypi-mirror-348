"""Type definitions for OpenAI Chat provider-specific content blocks."""

from typing import TYPE_CHECKING, Any, Sequence, TypedDict, Union

if TYPE_CHECKING:
    # -- OpenAIChat --
    from openai.types.chat import (
        ChatCompletionMessageToolCallParam as OpenAIChatToolUseBlockParam,
    )
    from openai.types.chat.chat_completion_content_part_image_param import (
        ChatCompletionContentPartImageParam as OpenAIChatCompletionContentPartImageParam,
    )
    from openai.types.chat.chat_completion_content_part_image_param import (
        ImageURL as OpenAIChatImageURL,
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
    OpenAIChatCompletionContentPartImageParam = Any
    OpenAIChatImageURL = Any


# OpenAI content block types
OpenAIChatContentBlock = Union[
    OpenAIChatCompletionContentPartParam,
    OpenAIChatCompletionContentPartImageParam,
    OpenAIChatToolUseBlockParam,
    OpenAIChatToolResponseParam,
]

# Provider-specific block sequences (for grouping operations)
OpenAIChatContentBlockSequence = Sequence[Sequence[OpenAIChatContentBlock]]


class OpenAIChatMessagesParam(TypedDict):
    messages: list[OpenAIChatContentBlock]
