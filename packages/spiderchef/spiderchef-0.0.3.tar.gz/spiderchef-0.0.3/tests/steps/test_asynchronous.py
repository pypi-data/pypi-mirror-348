from unittest.mock import patch

import pytest
from curl_cffi import Response
from pytest_httpbin.serve import Server
from tests.conftest import MockRecipe

from spiderchef.exceptions import ResponseIsNotOkError
from spiderchef.recipe import Recipe
from spiderchef.steps.asynchronous import FetchStep, SleepStep


@pytest.mark.asyncio
async def test_fetch_step(httpbin: Server) -> None:
    """Test fetch step using httpbin"""
    with patch(
        "spiderchef.steps.asynchronous.log"
    ):  # Patch logger to avoid output during tests
        recipe = Recipe(base_url=httpbin.url, name="test_recipe", steps=[])

        # Test GET request
        step = FetchStep(
            name="test_fetch",
            path="/get",
            method="GET",
            params={"key": "value"},
            return_type="text",
        )

        result = await step.execute(recipe, None)
        assert recipe.text_response
        assert result

        # Test GET request response
        step = FetchStep(
            name="test_fetch",
            path="/get",
            method="GET",
            params={"key": "value"},
            return_type="response",
        )

        result = await step.execute(recipe, None)
        assert isinstance(result, Response)

        # Test POST request with JSON data
        step_post = FetchStep(
            name="test_post_json",
            path="/post",
            method="POST",
            json_data={"test": "data"},
            return_type="json",
        )

        result = await step_post.execute(recipe, None)
        assert result["json"]["test"] == "data"

        await recipe.close()


@pytest.mark.asyncio
async def test_fetch_step_not_ok(httpbin: Server) -> None:
    """Test fetch step using httpbin"""
    with patch(
        "spiderchef.steps.asynchronous.log"
    ):  # Patch logger to avoid output during tests
        recipe = Recipe(base_url=httpbin.url, name="test_recipe", steps=[])

        # Test GET request
        step = FetchStep(
            name="test_fetch",
            path="/post",
            method="POST",
            data={"test": "data"},
            ok_status_codes=[],
        )
        with pytest.raises(ResponseIsNotOkError):
            await step.execute(recipe, None)
        await recipe.close()


@pytest.mark.asyncio
async def test_sleep(mock_recipe: MockRecipe) -> None:
    step = SleepStep(name="test_sleep")
    result = await step.execute(mock_recipe, None)
    assert result is None
