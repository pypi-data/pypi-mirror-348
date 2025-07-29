from typing import Awaitable, Callable, Literal, Optional, TypedDict, Union
from mindcontrol_types import PromptV1
from pydantic import BaseModel
from ..types import VersionTag


class Version(TypedDict):
    """Version type dict."""

    major: Optional[int]
    """Major version number."""
    minor: Optional[int]
    """Minor version number."""
    tag: Optional[VersionTag]
    """Version tag."""
    direct: Optional[bool]
    """If to use the direct API. If omitted, the default value will be used."""
    offline: Optional[bool]
    """If to use the offline API."""


VersionVariant = Union[Literal["exact"], Literal["offline"], VersionTag]
"""Version variant. Either "exact", "offline" or a version tag."""


class AWSKeys(BaseModel):
    """AWS provider keys."""

    access: str
    """Access key ID."""
    secret: str
    """Secret access key."""
    region: str
    """AWS region."""


class AzureKeys(BaseModel):
    """Azure provider keys."""

    resource: str
    """Resource ID."""
    key: str
    """API key."""


class ProviderKeys(BaseModel):
    """AI providers keys."""

    openai: Optional[str] = None
    """OpenAI keys."""
    aws: Optional[AWSKeys] = None
    """AWS keys."""
    azure: Optional[AzureKeys] = None
    """Azure keys."""
    anthropic: Optional[str] = None
    """Anthropic key."""
    gcp: Optional[str] = None
    """GCP key."""


Adapter = Callable[[ProviderKeys, PromptV1], Awaitable[Optional[str]]]
"""Adapter function."""
