from typing import Optional
from mindcontrol_types import PromptV1
from openai import AsyncOpenAI
from ..interop.openai import openai_interop
from .error import MissingKeys
from .types import ProviderKeys


async def openai_adapter(
    keys: ProviderKeys,
    prompt: PromptV1,
) -> Optional[str]:
    """OpenAI wrapper adapter.

    :param keys: Provider keys.
    :param prompt: Prompt object.

    :return: Response string if the adapter matches the prompt."""

    if prompt.settings is not None and prompt.settings.type != "openai":
        return None

    if keys.openai is None:
        raise MissingKeys("OpenAI API key is missing.")

    openai = AsyncOpenAI(api_key=keys.openai)
    interop = openai_interop(openai)

    return await interop(prompt)
