import re
from typing import List
from mindcontrol_types import PromptMessageV1, PromptV1
from .types import TemplateVars


def interpolate_string(prompt: str, vars: TemplateVars) -> str:
    """Interpolates variables into the prompt template string.

    :param prompt: Prompt template string.
    :param vars: Variables map to interpolate into the prompt.

    :return: Interpolated prompt string."""

    pattern = re.compile(r"\{{\s*(.*?)\s*}}")

    def replacer(match):
        key = match.group(1)
        return str(vars.get(key, match.group(0)))

    return pattern.sub(replacer, prompt)


def interpolate_messages(
    messages: List[PromptMessageV1], vars: TemplateVars
) -> List[PromptMessageV1]:
    """Interpolates variables into prompt messages.

    :param messages: List of prompt messages.
    :param vars: Variables map to interpolate into the messages.

    :return: Interpolated prompt messages."""

    return [
        PromptMessageV1(
            role=message.role,
            content=interpolate_string(message.content, vars),
        )
        for message in messages
    ]


def interpolate_prompt(prompt: PromptV1, vars: TemplateVars) -> PromptV1:
    """Interpolates variables into a prompt object.

    :param prompt: Prompt object.
    :param vars: Variables map to interpolate into the prompt.

    :return: Interpolated prompt object."""

    system = interpolate_string(prompt.system, vars) if prompt.system else prompt.system
    messages = interpolate_messages(prompt.messages, vars)

    return PromptV1(settings=prompt.settings, system=system, messages=messages)
