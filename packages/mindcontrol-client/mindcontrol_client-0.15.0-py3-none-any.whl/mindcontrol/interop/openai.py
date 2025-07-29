from typing import List
from mindcontrol_types import PromptMessageV1, PromptV1
from ..types import Interop
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam


def openai_interop(openai: AsyncOpenAI) -> Interop:
    async def interop(params: PromptV1) -> str:
        # [TODO] Throw an error?
        model = (
            params.settings.model
            if params.settings and params.settings.model
            else "gpt-4o"
        )

        messages: List[ChatCompletionMessageParam] = []
        if params.system:
            messages.append({"role": "system", "content": params.system})

        def message_dict(message: PromptMessageV1):
            return message.model_dump()

        messages.extend(map(message_dict, params.messages))

        response = await openai.chat.completions.create(model=model, messages=messages)
        choice = response.choices[0]
        return choice.message.content if choice and choice.message.content else ""

    return interop
