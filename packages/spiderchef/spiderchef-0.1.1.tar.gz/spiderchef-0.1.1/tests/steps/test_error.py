from typing import Any, NoReturn
from unittest.mock import patch

import pytest
from tests.conftest import MockRecipe

from spiderchef.steps.base import SyncStep
from spiderchef.steps.error import TryCatchStep


class SuccessStep(SyncStep):
    """Step that succeeds and returns a specified value."""

    return_value: str = "success"

    def _execute(self, recipe, previous_output=None) -> str:
        return self.return_value


class FailStep(SyncStep):
    """Step that raises an exception."""

    error_message: str = "Test error"
    error_type: type = ValueError

    def _execute(self, recipe, previous_output=None) -> NoReturn:
        raise self.error_type(self.error_message)


class CaptureErrorStep(SyncStep):
    """Step that captures error information from variables."""

    def _execute(self, recipe, previous_output=None) -> dict[str, Any | None]:
        return {
            "error": recipe.variables.get("error"),
            "error_type": recipe.variables.get("error_type"),
        }


@pytest.mark.asyncio
async def test_try_catch_step_success() -> None:
    """Test TryCatchStep when try steps succeed."""
    mock_recipe = MockRecipe()

    step = TryCatchStep(
        name="test_try_catch",
        try_steps=[
            SuccessStep(name="success_step_1", return_value="step1"),
            SuccessStep(name="success_step_2", return_value="step2"),
        ],
        catch_steps=[SuccessStep(name="catch_step", return_value="catch")],
        finally_steps=[SuccessStep(name="finally_step", return_value="finally")],
    )

    result = await step.execute(mock_recipe, "input")  # type: ignore

    # If try steps succeed, catch steps aren't executed
    # The final result should be from the finally steps
    assert result == "finally"
    # Error variables should not be set
    assert "error" not in mock_recipe.variables
    assert "error_type" not in mock_recipe.variables


@pytest.mark.asyncio
async def test_try_catch_step_exception() -> None:
    """Test TryCatchStep when try steps raise an exception."""
    mock_recipe = MockRecipe()

    with patch(
        "spiderchef.steps.error.log"
    ):  # Patch logger to avoid output during tests
        step = TryCatchStep(
            name="test_try_catch_exception",
            try_steps=[
                SuccessStep(name="success_step", return_value="step1"),
                FailStep(
                    name="fail_step",
                    error_message="Test failure",
                    error_type=ValueError,
                ),
                SuccessStep(name="unreached_step", return_value="unreached"),
            ],
            catch_steps=[
                CaptureErrorStep(name="capture_error"),
                SuccessStep(name="catch_step", return_value="caught"),
            ],
            finally_steps=[SuccessStep(name="finally_step", return_value="finally")],
        )

        result = await step.execute(mock_recipe, "input")  # type: ignore

        # The final result should be from the finally steps
        assert result == "finally"
        # Error variables should be set
        assert mock_recipe.variables["error"] == "Test failure"
        assert mock_recipe.variables["error_type"] == "ValueError"


@pytest.mark.asyncio
async def test_try_catch_step_no_catch_or_finally() -> None:
    """Test TryCatchStep with minimal configuration."""
    mock_recipe = MockRecipe()

    step = TryCatchStep(
        name="test_minimal",
        try_steps=[SuccessStep(name="success_step", return_value="success")],
    )

    result = await step.execute(mock_recipe, "input")  # type: ignore
    assert result == "success"


@pytest.mark.asyncio
async def test_try_catch_step_with_async_steps() -> None:
    """Test TryCatchStep with a mix of sync and async steps."""
    from spiderchef.steps.asynchronous import SleepStep

    mock_recipe = MockRecipe()

    step = TryCatchStep(
        name="test_with_async",
        try_steps=[
            SuccessStep(name="sync_step", return_value="sync"),
            SleepStep(name="sleep_step", timeout=1),
        ],
        finally_steps=[SuccessStep(name="final_step", return_value="final")],
    )

    result = await step.execute(mock_recipe, "start")  # type: ignore
    assert result == "final"
