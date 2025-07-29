import os
import tempfile
from pathlib import Path
from typing import Any, Generator

import pytest
import yaml
from pytest_httpbin.serve import Server
from typer.testing import CliRunner

from spiderchef.cli import app
from spiderchef.settings import BASE_RECIPE


class TestCli:
    @pytest.fixture
    def runner(self) -> CliRunner:
        return CliRunner()

    @pytest.fixture
    def sample_recipe_dict(self, httpbin: Server) -> dict[str, Any]:
        """Create a sample recipe config that uses the local httpbin server"""
        return {
            "name": "test_recipe",
            "base_url": httpbin.url,
            "steps": [
                {
                    "type": "fetch",
                    "name": "fetch_page",
                    "path": "/get",
                    "return_type": "json",
                },
                {"type": "extract_json", "name": "extract_url", "expression": "url"},
            ],
        }

    @pytest.fixture
    def sample_recipe_file(
        self, sample_recipe_dict: dict[str, Any]
    ) -> Generator[str, Any, None]:
        """Create a temporary YAML file with the sample recipe"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_recipe_dict, f)
            recipe_path = f.name

        yield recipe_path
        # Cleanup
        os.unlink(recipe_path)

    def test_recipe_new_command(self, runner: CliRunner) -> None:
        """Test the 'recipe new' command creates a new recipe file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            expected_file = Path(temp_dir) / "config_test.yaml"
            path = str(expected_file)
            result = runner.invoke(app, ["recipe", "new", "-o", path])

            print(path)
            assert result.exit_code == 0

            # Check if file was created
            assert expected_file.exists()

            # Verify content
            with open(expected_file) as f:
                content = yaml.safe_load(f)
                assert content == BASE_RECIPE

    def test_recipe_validate_command_valid(
        self, runner: CliRunner, sample_recipe_file: str
    ) -> None:
        """Test the 'recipe validate' command with valid recipe"""
        result = runner.invoke(app, ["recipe", "validate", sample_recipe_file])
        assert result.exit_code == 0

    def test_recipe_validate_command_invalid(self, runner: CliRunner) -> None:
        """Test the 'recipe validate' command with invalid recipe"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content")
            invalid_recipe = f.name

        try:
            result = runner.invoke(app, ["recipe", "validate", invalid_recipe])
            assert result.exit_code != 0  # Should fail validation
        finally:
            os.unlink(invalid_recipe)

    def test_cook_command(
        self, runner: CliRunner, sample_recipe_file: str, httpbin: Server
    ) -> None:
        """Test the 'cook' command processes a recipe and creates output using httpbin"""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "output.yaml"

            # Run command with real processing
            result = runner.invoke(
                app, ["cook", sample_recipe_file, "--output-file", str(output_file)]
            )

            # Verify command ran successfully
            assert result.exit_code == 0

            # Verify output file exists with expected content from httpbin
            assert output_file.exists()
            with open(output_file) as f:
                content = yaml.safe_load(f)
                # The output should contain the URL from the httpbin server
                assert httpbin.url in content, (
                    f"Expected URL not found in output: {content}"
                )

    def test_cook_command_with_post(self, runner: CliRunner, httpbin: Server) -> None:
        """Test the cook command with a POST request to httpbin"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            # Create recipe that posts data
            post_recipe = {
                "name": "test_post_recipe",
                "base_url": httpbin.url,
                "steps": [
                    {
                        "type": "fetch",
                        "name": "post_data",
                        "path": "/post",
                        "method": "POST",
                        "json_data": {"test": "data"},
                        "return_type": "json",
                    },
                    {
                        "type": "extract_json",
                        "name": "extract_json",
                        "expression": "json",
                    },
                ],
            }
            yaml.dump(post_recipe, f)
            recipe_path = f.name

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                output_file = Path(temp_dir) / "output.yaml"

                # Run command
                result = runner.invoke(
                    app, ["cook", recipe_path, "--output-file", str(output_file)]
                )

                # Verify command ran successfully
                assert result.exit_code == 0

                # Verify output contains the posted data reflected back from httpbin
                with open(output_file) as f:
                    content = yaml.safe_load(f)
                    assert content.get("test") == "data", (
                        f"Expected POST data not found: {content}"
                    )
        finally:
            os.unlink(recipe_path)

    def test_cook_command_with_error_status(
        self, runner: CliRunner, httpbin: Server
    ) -> None:
        """Test cook command handling of error status codes"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            # Create recipe that triggers an error
            error_recipe = {
                "name": "test_error_recipe",
                "base_url": httpbin.url,
                "steps": [
                    {
                        "type": "fetch",
                        "name": "fetch_error",
                        "path": "/status/404",
                        "return_type": "text",
                    }
                ],
            }
            yaml.dump(error_recipe, f)
            recipe_path = f.name

        try:
            result = runner.invoke(app, ["cook", recipe_path])

            # Command should complete but with logged error
            assert result.exit_code == 0
            # Can't easily check for the actual error message in CLI output
            # without more complex capture mechanisms
        finally:
            os.unlink(recipe_path)

    def test_cook_command_with_headers(self, runner: CliRunner, httpbin: Server):
        """Test cook command with custom headers"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            # Create recipe that uses headers
            headers_recipe = {
                "name": "test_headers_recipe",
                "base_url": httpbin.url,
                "steps": [
                    {
                        "type": "fetch",
                        "name": "fetch_with_headers",
                        "path": "/headers",
                        "headers": {"X-Test-Header": "test-value"},
                        "return_type": "json",
                    },
                    {
                        "type": "extract_json",
                        "name": "extract_headers",
                        "expression": "headers",
                    },
                ],
            }
            yaml.dump(headers_recipe, f)
            recipe_path = f.name

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                output_file = Path(temp_dir) / "output.yaml"

                # Run command
                result = runner.invoke(
                    app, ["cook", recipe_path, "--output-file", str(output_file)]
                )

                # Verify command ran successfully
                assert result.exit_code == 0

                # Verify output contains our custom header
                with open(output_file) as f:
                    content = yaml.safe_load(f)
                    headers = content
                    assert headers.get("X-Test-Header") == "test-value", (
                        f"Header not found in response: {headers}"
                    )
        finally:
            os.unlink(recipe_path)
