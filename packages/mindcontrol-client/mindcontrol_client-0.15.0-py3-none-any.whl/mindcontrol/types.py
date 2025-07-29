from typing import Callable, Awaitable, Dict, Literal, Union
from mindcontrol_types import PromptV1

Interop = Callable[[PromptV1], Awaitable[str]]
"""Prompt interop function."""

TemplateVars = Dict[str, Union[str, int, float, bool, None]]
"""Prompt template variables."""

VersionTag = Union[Literal["published"], Literal["any"]]
"""Version tag."""
