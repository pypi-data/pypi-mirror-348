import os
import tempfile
from typing import Any, Generator

import pytest
import yaml
from pytest_httpbin.serve import Server

from spiderchef.recipe import Recipe


class TestRecipe:
    @pytest.fixture
    def basic_recipe_dict(self, httpbin: Server) -> dict[str, Any]:
        """Create a simple recipe that fetches from httpbin"""
        return {
            "name": "test_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "fetch",
                    "name": "fetch_main_page",
                    "path": "/get",
                    "return_type": "json",
                },
                {"type": "extract_json", "name": "extract_url", "expression": "url"},
            ],
        }

    @pytest.fixture
    def basic_recipe_file(
        self, basic_recipe_dict: dict[str, Any]
    ) -> Generator[str, Any, None]:
        """Create a temporary file with the basic recipe"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(basic_recipe_dict, f)
            recipe_path = f.name

        yield recipe_path
        # Cleanup
        os.unlink(recipe_path)

    @pytest.fixture
    def advanced_recipe_dict(self, httpbin: Server) -> dict[str, Any]:
        """Create a more complex recipe with multiple step types"""
        return {
            "name": "advanced_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "fetch",
                    "name": "fetch_html",
                    "path": "/html",
                    "return_type": "text",
                },
                {"type": "remove_html_tags", "name": "clean_html"},
                {"type": "remove_extra_whitespace", "name": "clean_text"},
            ],
        }

    @pytest.fixture
    def advanced_recipe_file(
        self, advanced_recipe_dict: dict[str, Any]
    ) -> Generator[str, Any, None]:
        """Create a temporary file with the advanced recipe"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(advanced_recipe_dict, f)
            recipe_path = f.name

        yield recipe_path
        # Cleanup
        os.unlink(recipe_path)

    def test_from_yaml(
        self, basic_recipe_file: str, basic_recipe_dict: dict[str, Any]
    ) -> None:
        """Test loading recipe from YAML file"""
        recipe = Recipe.from_yaml(basic_recipe_file)

        assert recipe.name == basic_recipe_dict["name"]
        assert recipe.base_url == basic_recipe_dict["base_url"]
        assert len(recipe.steps) == len(basic_recipe_dict["steps"])
        assert recipe.steps[0].name == basic_recipe_dict["steps"][0]["name"]
        assert recipe.steps[1].name == basic_recipe_dict["steps"][1]["name"]

    @pytest.mark.asyncio
    async def test_basic_recipe_cook(
        self, basic_recipe_file: str, httpbin: Server
    ) -> None:
        """Test cooking a basic recipe against httpbin"""
        recipe = Recipe.from_yaml(basic_recipe_file)

        # The recipe should extract the URL from httpbin response
        result = await recipe.cook()

        # The result should be the URL used to make the request
        assert httpbin.url in result

    @pytest.mark.asyncio
    async def test_advanced_recipe_cook(
        self, advanced_recipe_file: str, httpbin: Server
    ) -> None:
        """Test cooking a more complex recipe with chained transformations"""
        recipe = Recipe.from_yaml(advanced_recipe_file)

        # This recipe fetches HTML from httpbin and cleans it
        result = await recipe.cook()

        # The result should be cleaned HTML with whitespace normalized
        assert result is not None
        assert "<html>" not in result, "HTML tags should be removed"
        assert "  " not in result, "Extra whitespace should be removed"
        assert "Herman Melville" in result, "Expected content from httpbin HTML missing"

    @pytest.mark.asyncio
    async def test_recipe_with_post_request(self, httpbin: Server):
        """Test recipe with POST request to httpbin"""
        # Create recipe directly
        recipe_dict = {
            "name": "post_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "fetch",
                    "name": "post_data",
                    "path": "/post",
                    "method": "POST",
                    "json_data": {"test_key": "test_value"},
                    "return_type": "json",
                },
                {"type": "extract_json", "name": "extract_data", "expression": "json"},
            ],
        }

        recipe = Recipe(**recipe_dict)

        # Execute recipe
        result = await recipe.cook()

        # Verify posted data is reflected in response
        assert result.get("test_key") == "test_value"

    @pytest.mark.asyncio
    async def test_recipe_with_headers(self, httpbin: Server):
        """Test recipe sending custom headers to httpbin"""
        recipe_dict = {
            "name": "headers_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "fetch",
                    "name": "fetch_with_headers",
                    "path": "/headers",
                    "headers": {"X-Custom-Header": "test-value"},
                    "return_type": "json",
                },
                {
                    "type": "extract_json",
                    "name": "extract_headers",
                    "expression": "headers",
                },
            ],
        }

        recipe = Recipe(**recipe_dict)

        # Execute recipe
        result = await recipe.cook()

        # Verify our custom header is in the response
        assert result.get("X-Custom-Header") == "test-value"

    @pytest.mark.asyncio
    async def test_recipe_with_cookies(self, httpbin: Server):
        """Test recipe handling cookies"""
        recipe_dict = {
            "name": "cookies_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "fetch",
                    "name": "set_cookies",
                    "path": "/cookies/set?test_cookie=cookie_value",
                    "return_type": "json",
                },
                {
                    "type": "fetch",
                    "name": "check_cookies",
                    "path": "/cookies",
                    "return_type": "json",
                },
                {
                    "type": "extract_json",
                    "name": "extract_cookies",
                    "expression": "cookies",
                },
            ],
        }

        recipe = Recipe(**recipe_dict)

        # Execute recipe
        result = await recipe.cook()

        # Verify cookie is maintained between requests
        assert result.get("test_cookie") == "cookie_value"

    @pytest.mark.asyncio
    async def test_recipe_error_handling(self, httpbin: Server):
        """Test recipe handles errors appropriately"""
        recipe_dict = {
            "name": "error_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "fetch",
                    "name": "fetch_error",
                    "path": "/status/404",
                    "return_type": "text",
                    "ok_status_codes": [200],  # Will raise error on 404
                }
            ],
        }

        recipe = Recipe(**recipe_dict)

        # The recipe should raise an exception
        with pytest.raises(Exception):
            await recipe.cook()

    @pytest.mark.asyncio
    async def test_recipe_error_handling_nonexistent_step(self, httpbin: Server):
        """Test recipe handles errors appropriately"""
        recipe_dict = {
            "name": "error_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "*****",  # Will raise error since it does not exist
                    "name": "fetch_error",
                    "path": "/status/404",
                    "return_type": "text",
                    "ok_status_codes": [200],
                }
            ],
        }
        # The recipe should raise an exception
        with pytest.raises(ValueError):
            Recipe(**recipe_dict)
