from typing import Literal
from unittest.mock import MagicMock

import pytest

from spiderchef.steps.base import AsyncStep, SaveStep, SyncStep


@pytest.mark.asyncio
async def test_sync_step_execution() -> None:
    """Test that SyncStep wraps sync execution in an async context"""

    class TestSyncStep(SyncStep):
        def _execute(self, recipe, previous_output=None) -> Literal["test_result"]:
            return "test_result"

    step = TestSyncStep(name="test_step")
    result = step.execute(MagicMock(), None)
    assert result == "test_result"


@pytest.mark.asyncio
async def test_async_step_execution() -> None:
    """Test that AsyncStep handles async execution"""

    class TestAsyncStep(AsyncStep):
        async def _execute(
            self, recipe, previous_output=None
        ) -> Literal["async_result"]:
            return "async_result"

    step = TestAsyncStep(name="test_async_step")
    result = await step.execute(MagicMock(), None)
    assert result == "async_result"


def test_save_step_execution() -> None:
    """Test that SaveStep correctly saves correctly to variables"""
    mock = MagicMock()
    mock.variables = {}
    step = SaveStep(variable="hello")
    result = step.execute(mock, "there")
    assert result == "there"
    assert mock.variables
    assert mock.variables["hello"] == "there"
