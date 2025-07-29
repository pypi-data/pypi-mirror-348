from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Literal

from curl_cffi import Response
from pydantic import Field
from structlog import get_logger

from spiderchef.exceptions import ResponseIsNotOkError
from spiderchef.steps.base import AsyncStep

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe

log = get_logger()


class FetchStep(AsyncStep):
    """Step to fetch data from an API."""

    assign_to_base: bool = True
    return_type: Literal["text", "json", "response"] = "text"
    method: Literal["GET", "POST"] = "GET"
    path: str = ""
    params: dict[str, Any] = Field(default_factory=dict)
    json_data: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] | str = Field(default_factory=dict)
    headers: dict[str, Any] = Field(default_factory=dict)
    ok_status_codes: list[int] = Field(default_factory=lambda: [200])
    timeout: int = 5

    def validate_response(self, response: Response):
        if response.status_code not in self.ok_status_codes:
            raise ResponseIsNotOkError(response.status_code)

    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        session = await recipe.session
        match self.method:
            case "GET":
                response = await session.get(
                    url=self.path,
                    params=self.params,
                    timeout=self.timeout,
                    headers=self.headers,
                )
            case "POST":
                if self.data:
                    response = await session.post(
                        url=self.path,
                        params=self.params,
                        data=self.data,
                        timeout=self.timeout,
                        headers=self.headers,
                    )
                else:
                    response = await session.post(
                        url=self.path,
                        params=self.params,
                        json=self.json_data,
                        timeout=self.timeout,
                        headers=self.headers,
                    )
        self.validate_response(response)
        if self.assign_to_base:
            recipe.text_response = response.text
        if self.return_type == "json" and self.assign_to_base:
            recipe.json_response = response.json()
        match self.return_type:
            case "json":
                return response.json()
            case "text":
                return response.text
            case "response":
                return response


class SleepStep(AsyncStep):
    timeout: int = 3

    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        await asyncio.sleep(self.timeout)
        return previous_output
