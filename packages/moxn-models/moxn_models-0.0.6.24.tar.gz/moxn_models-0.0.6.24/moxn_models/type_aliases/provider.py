from typing_extensions import Sequence

from moxn_models.type_aliases.anthropic import AnthropicContentBlock
from moxn_models.type_aliases.google import GoogleContentBlock
from moxn_models.type_aliases.openai_chat import OpenAIChatContentBlock

ProviderContentBlock = (
    AnthropicContentBlock | OpenAIChatContentBlock | GoogleContentBlock
)


ProviderContentBlockSequence = Sequence[Sequence[ProviderContentBlock]]
