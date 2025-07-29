from __future__ import annotations

from typing import Any, ClassVar, Literal

import yaml
from curl_cffi import BrowserTypeLiteral, CurlHttpVersion
from curl_cffi.requests import AsyncSession, Response
from lxml.etree import _ElementTree
from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic_extra_types.semantic_version import SemanticVersion
from structlog import get_logger

from spiderchef.steps import STEP_REGISTRY, AsyncStep, BaseStep
from spiderchef.utils import convert_steps

log = get_logger()


# TBD: Proxies still need to be fully integrated
class Proxy(BaseModel):
    proxy_url: HttpUrl | None = None
    username: str | None = None
    password: str | None = None


class Recipe(BaseModel):
    step_registry: ClassVar[dict[str, type[BaseStep]]] = STEP_REGISTRY
    name: str = "test_recipe"
    version: SemanticVersion = SemanticVersion(1)
    base_url: str
    http_version: Literal["1", "1.1", "2", "3"] = "2"
    impersonate: BrowserTypeLiteral = "firefox"
    default_encoding: str = "utf-8"
    _session: AsyncSession | None = None
    _base_response: Response | None = None
    _tree: _ElementTree | None = None
    json_response: Any = None
    text_response: str | None = None
    headers: dict = Field(default_factory=dict)
    proxies: list[Proxy] = Field(default_factory=list)
    steps: list[BaseStep]

    @classmethod
    def from_yaml(cls, file_path: str) -> "Recipe":
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return cls(**data)

    @field_validator("steps", mode="before")
    def convert_step_dicts(cls, value: list[dict]) -> list[BaseStep]:
        """Convert step dictionaries to Step instances before model creation."""
        return convert_steps(cls.step_registry, value)

    @property
    async def session(self) -> AsyncSession:
        if not self._session:
            match self.http_version:  # pragma: no cover
                case "2":
                    http_version = CurlHttpVersion.V2TLS
                case "1.1":
                    http_version = CurlHttpVersion.V1_1
                case "1":
                    http_version = CurlHttpVersion.V1_0
                case "3":
                    http_version = CurlHttpVersion.V3
            self._session = AsyncSession(
                base_url=self.base_url,
                http_version=http_version,
                impersonate=self.impersonate,
                default_encoding=self.default_encoding,
            )
            await self._session.__aenter__()
        return self._session

    async def close(self) -> None:
        if self._session:
            await self._session.__aexit__(None, None, None)

    async def cook(self) -> Any:
        output = None
        log.info(f"🥣🥄🔥 Cooking '{self.name}' recipe!")
        try:
            for step_number, step in enumerate(self.steps, start=1):
                log.info(
                    f"➡️  {step_number}. {step.name}...",
                    step_class=step.__class__.__name__,
                )
                if issubclass(type(step), AsyncStep):
                    output = await step.execute(self, output)
                else:
                    output = step.execute(self, output)
        except Exception as e:
            await self.close()
            raise e
        await self.close()
        log.info(f"🍞 '{self.name}' recipe finished", output=output)
        return output
