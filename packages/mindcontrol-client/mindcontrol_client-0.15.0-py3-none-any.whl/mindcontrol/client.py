import asyncio
import ssl
import time
import logging
from typing import Optional
import aiohttp
import certifi
from mindcontrol_types import (
    CollectionParsedV1,
    CollectionSettings,
    CollectionV1,
    PayloadV1,
    ResourceV1,
)
from .error import InvalidVersion, MissingOfflineCollection
from .template import interpolate_prompt, interpolate_string
from .types import Interop, TemplateVars, VersionTag

logger = logging.getLogger(__name__)


class MindControl:
    """Mind Control client class."""

    token: str
    """Token string."""
    endpoint: str
    """API endpoint."""
    direct: bool
    """If to use the direct API by default. Direct is the API that has slightly
    more latency but always returns the latest data."""

    def __init__(
        self,
        token: str,
        endpoint: str = "https://api.mindcontrol.studio",
        direct: bool = False,
    ):
        """Client constructor.

        :param token: Token string.
        :param endpoint: API endpoint. Must not end with slash.
        :param direct: If to use the direct API by default. Direct is the API that has slightly more latency but always returns the latest data.
        """
        self._sync = None
        self.token = token
        self.endpoint = endpoint
        self.direct = direct

    async def get(
        self,
        collection_id: str,
        major: Optional[int] = None,
        minor: Optional[int] = None,
        tag: Optional[VersionTag] = None,
        direct: Optional[bool] = None,
    ) -> CollectionParsedV1:
        """Fetches and parses collection version.

        :param collection_id: Collection id.
        :param major: Major version number.
        :param minor: Minor version number.
        :param tag: Version tag.
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: Collection instance."""

        url = self.url(collection_id, major, minor, tag, direct)
        headers = {"Authorization": f"Bearer {self.token}"}

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        ) as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    # [TODO] Handle and process the error.
                    raise Exception(f"HTTP Error: {response.status}")

                text = await response.text()
                return MindControlCollection.parse_json(text)

    async def payload(
        self,
        collection_id: str,
        major: Optional[int] = None,
        minor: Optional[int] = None,
        tag: Optional[VersionTag] = None,
        direct: Optional[bool] = None,
    ) -> PayloadV1:
        """Fetches and parses collection payload.

        :param collection_id: Collection id.
        :param major: Major version number.
        :param minor: Minor version number.
        :param tag: Version tag.
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: Payload instance."""

        collection = await self.get(
            collection_id=collection_id,
            major=major,
            minor=minor,
            tag=tag,
            direct=direct,
        )
        return collection.payload

    def url(
        self,
        collection_id: str,
        major: Optional[int] = None,
        minor: Optional[int] = None,
        tag: Optional[VersionTag] = None,
        direct: Optional[bool] = None,
    ) -> str:
        """Generates API URL for the collection version.

        :param collection_id: Collection id.
        :param major: Major version number.
        :param minor: Minor version number.
        :param tag: Version tag.
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: API URL for the collection version."""

        segments = [collection_id]

        # [TODO] Add tests
        if minor is not None:
            if tag:
                raise InvalidVersion("Minor version cannot be used with version tag.")
            if major is None:
                raise InvalidVersion(
                    "Minor version cannot be used without major version."
                )

        if major is not None:
            version = f"v{major}"
            if minor is not None:
                version += f".{minor}"
            segments.append(version)

        if tag:
            segments.append(tag)

        if len(segments) == 1:
            segments.append("published")

        direct = direct if direct is not None else self.direct
        if direct:
            segments.append("direct")

        return f"{self.endpoint}/payloads/{'/'.join(segments)}"

    def collection(
        self,
        id: str,
        major: Optional[int] = None,
        minor: Optional[int] = None,
        tag: Optional[VersionTag] = None,
        direct: Optional[bool] = None,
        offline: Optional[bool] = None,
        collection_json: Optional[str] = None,
        *,
        timeout: Optional[float] = None,
        cache: Optional[float] = None,
    ) -> "MindControlCollection":
        """
        Creates collection instance.

        :param collection_id: Collection id.
        :param major: Major version number.
        :param minor: Minor version number.
        :param tag: Version tag.
        :param direct: If to use the direct API. If omitted, the default value will be used.
        :param offline: If to use the offline API.
        :param collection_json: The collection JSON to fallback to or use in offline mode.
        :param timeout: Request timeout in seconds (default: 5 seconds).
        :param cache: Cache duration in seconds for successful responses (default: 15 minutes).

        :return: Collection instance."""

        return MindControlCollection(
            client=self,
            id=id,
            major=major,
            minor=minor,
            tag=tag,
            direct=direct,
            offline=offline,
            collection_json=collection_json,
            timeout=timeout,
            cache=cache,
        )

    @property
    def sync(self):
        """Returns instance with synchronous methods.

        :return: Synchronous methods instance."""

        if self._sync is None:

            self._sync = MindControlSyncMethods(self)

        return self._sync


class MindControlSyncMethods:
    """Mind Control client synchronous methods class."""

    def __init__(self, instance):
        self._instance = instance

    def get(self, *args, **kwargs):
        """Fetches and parses collection version. Synchronous version.

        :param collection_id: Collection id.
        :param major: Major version number.
        :param minor: Minor version number.
        :param tag: Version tag.
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: Collection instance."""

        return asyncio.run(self._instance.get(*args, **kwargs))

    def payload(self, *args, **kwargs):
        """Fetches and parses collection payload. Synchronous version.

        :param collection_id: Collection id.
        :param major: Major version number.
        :param minor: Minor version number.
        :param tag: Version tag.
        :param direct: If to use the direct API. If omitted, the default value will be used.

        :return: Payload instance."""

        return asyncio.run(self._instance.payload(*args, **kwargs))


class MindControlCollection:
    """Mind Control collection class."""

    client: MindControl
    """Mind Control client instance."""
    id: str
    """Collection id."""
    major: Optional[int] = None
    """Major version number."""
    minor: Optional[int] = None
    """Minor version number."""
    tag: Optional[VersionTag] = None
    """Version tag."""
    direct: Optional[bool] = None
    """If to use the direct API. If omitted, the default value will be used."""
    offline: Optional[bool] = None
    """If to use the offline API."""
    collection: Optional[CollectionParsedV1] = None
    """The collection to fallback to or use in offline mode."""

    def __init__(
        self,
        client: MindControl,
        id: str,
        major: Optional[int] = None,
        minor: Optional[int] = None,
        tag: Optional[VersionTag] = None,
        direct: Optional[bool] = None,
        offline: Optional[bool] = None,
        collection_json: Optional[str] = None,
        *,
        timeout: Optional[float] = None,
        cache: Optional[float] = None,
    ):
        """Collection constructor.

        :param client: Mind Control client.
        :param id: Collection id.
        :param major: Major version number.
        :param minor: Minor version number.
        :param tag: Version tag.
        :param direct: If to use the direct API. If omitted, the default value will be used.
        :param offline: If to use the offline API.
        :param collection_json: The collection JSON to fallback to or use in offline mode.
        :param timeout: Request timeout in seconds (default: 5 seconds).
        :param cache: Cache duration in seconds for successful responses (default: 15 minutes).
        """

        self._sync = None
        self.client = client
        self.id = id
        self.major = major
        self.minor = minor
        self.tag = tag
        self.direct = direct
        self.offline = offline

        if collection_json:
            self.collection = MindControlCollection.parse_json(collection_json)

        if self.offline and collection_json is None:
            raise MissingOfflineCollection()

        self.timeout = timeout if timeout is not None else 5.0

        self.cache_duration = cache if cache is not None else 60.0 * 15.0
        self._cache: Optional[CollectionParsedV1] = None
        self._cache_expiry = 0.0

    async def get(self) -> CollectionParsedV1:
        """Fetches and parses collection version.

        :return: Collection instance."""

        # Return cached collection in offline mode
        if self.offline and self.collection:
            return self.collection

        # Return cached collection if not expired
        now = time.time()
        if self._cache is not None and now < self._cache_expiry:
            return self._cache

        try:
            collection = await asyncio.wait_for(
                self.client.get(
                    self.id,
                    major=self.major,
                    minor=self.minor,
                    tag=self.tag,
                    direct=self.direct,
                ),
                timeout=self.timeout,
            )
        except Exception as e:
            if self._cache is not None:
                # Fallback to cached collection
                logger.warning(
                    "Falling back to cached collection for '%s' due to error: %s",
                    self.id,
                    e,
                )
                return self._cache
            elif self.collection is not None:
                # Fallback to bundled collection
                logger.warning(
                    "Falling back to bundled collection for '%s' due to error: %s",
                    self.id,
                    e,
                )
                return self.collection
            else:
                raise

        # Cache successful response
        self._cache = collection
        self._cache_expiry = now + self.cache_duration

        return collection

    async def payload(self) -> PayloadV1:
        """Fetches and parses collection payload.

        :return: Payload instance."""

        collection = await self.get()
        return collection.payload

    async def find(self, name: str) -> Optional[ResourceV1]:
        """Fetches and parses collection version.

        :param name: Resource name.

        :return: Resource instance."""

        payload = await self.payload()

        for resource in payload.resources:
            if resource.var.name == name:
                return resource

        return None

    async def exec(
        self, name: str, interop: Interop, vars: Optional[TemplateVars] = None
    ) -> str:
        """Executes the given prompt or chain.

        :param name: Prompt or chain name to execute.
        :param interop: Prompt interop function.
        :param vars: Variables to use in the prompt or chain.

        :return: Result of the prompt execution."""

        resource = await self.find(name)

        if resource is not None:
            vars = vars if vars is not None else {}

            if resource.type == "prompt":
                prompt = interpolate_prompt(resource.prompt, vars)
                return await interop(prompt)

            elif resource.type == "chain":
                result = None
                for prompt in resource.chain:
                    prompt = prompt.model_copy()
                    prompt.system = prompt.system or resource.system
                    prompt.settings = prompt.settings or resource.settings

                    vars = {**vars, "result": result} if result else vars
                    result = await interop(interpolate_prompt(prompt, vars))
                return result or ""

        raise Exception(f'Prompt or chain "{name}" not found in the collection.')

    async def fragment(self, path: str, vars: Optional[TemplateVars] = None) -> str:
        """Finds and interpolates a fragment prompt by path.

        :param path: Path to the fragment prompt.
        :param vars: Prompt variables.

        :return: Interpolated prompt."""

        if "." not in path:
            raise ValueError(f'Invalid fragment prompt path "{path}".')

        fragments_name, name = path.split(".", 1)
        resource = await self.find(fragments_name)

        if resource is None or resource.type != "fragments":
            raise ValueError(
                f'Fragments resource "{fragments_name}" not found in the collection.'
            )

        fragment = next(
            (fragment for fragment in resource.fragments if fragment.var.name == name),
            None,
        )

        if fragment is None:
            raise ValueError(
                f'Fragment prompt "{name}" not found in the "{fragments_name}" fragments.'
            )

        return interpolate_string(fragment.content, vars if vars else {})

    @property
    def sync(self):
        """Returns instance with synchronous methods.

        :return: Synchronous methods instance."""

        if self._sync is None:
            self._sync = MindControlCollectionSyncMethods(self)

        return self._sync

    @staticmethod
    def parse_json(collection_json: str) -> CollectionParsedV1:
        """Parses collection JSON.

        :param collection_json: Collection JSON.

        :return: Collection instance."""

        collection = CollectionV1.model_validate_json(collection_json)

        payload = PayloadV1.model_validate_json(collection.payload)
        settings = None
        if collection.settings is not None:
            settings = CollectionSettings.model_validate_json(collection.settings)

        return CollectionParsedV1(
            v=collection.v,
            time=collection.time,
            major=collection.major,
            minor=collection.minor,
            draft=collection.draft,
            payload=payload,
            settings=settings,
        )


class MindControlCollectionSyncMethods:
    """Mind Control collection synchronous methods class."""

    def __init__(self, instance):
        self._instance = instance

    def get(self, *args, **kwargs):
        """Fetches and parses collection version.

        :return: Collection instance."""

        return asyncio.run(self._instance.get(*args, **kwargs))

    def payload(self, *args, **kwargs):
        """Fetches and parses collection payload.

        :return: Payload instance."""

        return asyncio.run(self._instance.payload(*args, **kwargs))

    def find(self, *args, **kwargs):
        """Fetches and parses collection version.

        :return: Resource instance."""

        return asyncio.run(self._instance.find(*args, **kwargs))

    def exec(self, *args, **kwargs):
        """Executes the given prompt or chain.

        :param name: Prompt or chain name to execute.
        :param interop: Prompt interop function.
        :param vars: Variables to use in the prompt or chain.

        :return: Result of the prompt execution."""

        return asyncio.run(self._instance.exec(*args, **kwargs))

    def fragment(self, *args, **kwargs) -> str:
        """Finds and interpolates a fragment prompt by path.

        :param path: Path to the fragment prompt.
        :param vars: Prompt variables.

        :return: Interpolated prompt."""

        return asyncio.run(self._instance.fragment(*args, **kwargs))
