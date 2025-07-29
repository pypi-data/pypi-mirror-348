from mindcontrol_types import PromptV1
from typing import List, Optional
from ..client import MindControl
from ..types import TemplateVars
from .types import AWSKeys, Adapter, AzureKeys, ProviderKeys, Version, VersionVariant
from .error import MissingAdapter


class MindControlWrapper:
    """Mind Control wrapper class."""

    adapters: List[Adapter]
    """List of active adapters."""
    keys: ProviderKeys
    """Provider keys."""
    client: MindControl
    """Mind Control client instance."""
    collection_id: str
    """Collection id."""
    collection_json: str
    """The collection JSON."""
    major: int
    """Major version number."""
    minor: int
    """Minor version number."""
    version: VersionVariant
    """Version variant."""
    direct: bool
    """If to use the direct API. If omitted, the default value will be used."""

    def __init__(
        self,
        adapters: List[Adapter],
        token: str,
        collection_id: str,
        collection_json: str,
        major: int,
        minor: int,
        endpoint: str = "https://api.mindcontrol.studio",
        version: VersionVariant = "published",
        direct: bool = False,
        openai: Optional[str] = None,
        aws: Optional[AWSKeys] = None,
        azure: Optional[AzureKeys] = None,
        anthropic: Optional[str] = None,
        gcp: Optional[str] = None,
    ):
        """Wrapper constructor.

        :param adapters: List of active adapters.
        :param token: Mind Control API token.
        :param collection_id: Collection id.
        :param collection_json: The collection JSON.
        :param major: Major version number.
        :param minor: Minor version number.
        :param version: Version variant.
        :param direct: If to use the direct API. If omitted, the default value will be used.
        :param openai: OpenAI API key.
        :param aws: AWS provider keys.
        :param azure: Azure provider keys.
        :param anthropic: Anthropic key.
        :param gcp: Google Cloud Platform key."""

        self.adapters = adapters
        self.keys = ProviderKeys(
            openai=openai, aws=aws, azure=azure, anthropic=anthropic, gcp=gcp
        )
        self.client = MindControl(token, endpoint=endpoint)
        self.collection_id = collection_id
        self.collection_json = collection_json
        self.major = major
        self.minor = minor
        self.version = version
        self.direct = direct

    async def exec(
        self,
        name: str,
        vars: Optional[TemplateVars] = None,
        version: Optional[VersionVariant] = None,
        direct: Optional[bool] = None,
    ) -> str:
        """Executes the given prompt or chain using one of the active
        adapters.

        :param name: Prompt or chain name to execute.
        :param vars: Variables to use in the prompt or chain.
        :param version: Version variant (tag or "exact").
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: Result of the prompt execution."""

        collection = self.client.collection(
            self.collection_id,
            collection_json=self.collection_json,
            **self.resolve_version(version, direct),
        )

        async def interop(prompt: PromptV1) -> str:
            for adapter in self.adapters:
                response = await adapter(self.keys, prompt)
                if response is not None:
                    return response

            raise MissingAdapter("No adapter matched the prompt.")

        return await collection.exec(name, interop=interop, vars=vars)

    async def fragment(
        self,
        path: str,
        vars: Optional[TemplateVars] = None,
        version: Optional[VersionVariant] = None,
        direct: Optional[bool] = None,
    ) -> str:
        """Finds and interpolates a fragment prompt by path..

        :param name: Fragment prompt path.
        :param vars: Variables to use in the prompt.
        :param version: Version variant (tag or "exact").
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: Interpolated prompt."""

        collection = self.client.collection(
            self.collection_id,
            collection_json=self.collection_json,
            **self.resolve_version(version, direct),
        )

        return await collection.fragment(path=path, vars=vars)

    def resolve_version(
        self,
        version: Optional[VersionVariant] = None,
        direct: Optional[bool] = None,
    ) -> Version:
        """Resolves the version variant.

        :param version: Version variant (tag, "exact" or "offline").
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: Version dict."""

        version = version or self.version
        direct = direct if direct is not None else self.direct

        if version == "published":
            return Version(
                major=self.major,
                minor=None,
                tag="published",
                direct=direct,
                offline=False,
            )
        elif version == "any":
            return Version(
                major=self.major,
                minor=None,
                tag="any",
                direct=direct,
                offline=False,
            )
        elif version == "exact":
            return Version(
                major=self.major,
                minor=self.minor,
                tag=None,
                direct=direct,
                offline=False,
            )
        elif version == "offline":
            return Version(
                major=self.major,
                minor=self.minor,
                tag=None,
                direct=False,
                offline=True,
            )