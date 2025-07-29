from typing import Any
from unittest.mock import MagicMock

import pytest
from tests.conftest import MockRecipe

from spiderchef.steps.conditional import CompareStep


@pytest.mark.parametrize(
    "input_value, compare_to, condition, expected",
    [
        (5, 3, "gt", True),
        (3, 5, "gt", False),
        (3, 3, "eq", True),
        ("abc", "abc", "eq", True),
        (5, 5, "lt", False),
        (5, 5, "lte", True),
        (5, 5, "gte", True),
    ],
)
@pytest.mark.asyncio
async def test_compare_step(
    input_value: Any,
    compare_to: Any,
    condition: str,
    expected: bool,
):
    step = CompareStep(name="test_compare", compare_to=compare_to, condition=condition)
    result = step.execute(MagicMock(), input_value)
    assert result == expected


@pytest.mark.parametrize(
    "input_value, condition, expected",
    [
        ({"hello": 3, "there": 5}, "gt", False),
        ({"hello": 3, "there": 5}, "gte", False),
        ({"hello": 3, "there": 5}, "lt", True),
        ({"hello": 3, "there": 5}, "lte", True),
        ({"hello": 3, "there": 5}, "eq", False),
    ],
)
@pytest.mark.asyncio
async def test_compare_json_step(
    input_value: Any,
    condition: str,
    expected: bool,
):
    step = CompareStep(
        name="test_compare", left_key="hello", right_key="there", condition=condition
    )
    result = step.execute(MagicMock(), input_value)
    assert result == expected


@pytest.mark.asyncio
async def test_compare_json_step_failure():
    step = CompareStep(
        name="test_compare", left_key="hello", right_key="there", condition="gt"
    )
    with pytest.raises(ValueError):
        step.execute(MagicMock(), {"hello": 3})


@pytest.mark.asyncio
async def test_compare_json_step_response(mock_recipe: MockRecipe) -> None:
    step = CompareStep(
        name="test_compare",
        left_key="hello",
        right_key="there",
        condition="gt",
        use_previous_output=False,
    )
    result = step.execute(MagicMock(), None)
    assert not result
