from typing import Any

import pytest
from tests.conftest import HTTPBIN_URL, MockRecipe

from spiderchef.steps.format import (
    JoinBaseUrl,
    RemoveExtraWhitespace,
    RemoveHTMLTags,
    ToFloat,
    ToInt,
    ToMoneyStep,
    ToStr,
)


@pytest.mark.parametrize(
    "step_class, input_value, expected_output",
    [
        (ToInt, "123", 123),
        (ToInt, "123.4", 123),
        (ToFloat, "123.45", 123.45),
        (ToStr, 123, "123"),
        (RemoveHTMLTags, "<p>text</p>", "text"),
        (RemoveExtraWhitespace, "  too   many    spaces  ", " too many spaces "),
    ],
)
@pytest.mark.asyncio
async def test_format_steps(
    step_class: ToInt | ToFloat | ToStr | RemoveHTMLTags | RemoveExtraWhitespace,
    input_value: Any,
    expected_output: Any,
    mock_recipe: MockRecipe,
) -> None:
    step = step_class(name=f"test_{step_class.__name__}")
    result = step.execute(mock_recipe, input_value)
    assert result == expected_output


@pytest.mark.parametrize(
    "step_class, input_value, thousands_separator, decimal_separator, expected_output",
    [
        (ToMoneyStep, "1.234,56", ".", ",", 1234.56),
        (ToMoneyStep, "1,234.56", ",", ".", 1234.56),
        (ToMoneyStep, "123.45", ",", ".", 123.45),
        (ToMoneyStep, "1.234", ".", ".", 1234),
        (ToMoneyStep, None, ",", ".", None),
        (ToMoneyStep, "aaa", ",", ".", None),
    ],
)
@pytest.mark.asyncio
async def test_format_steps_money(
    step_class: ToMoneyStep,
    input_value: Any,
    thousands_separator: str,
    decimal_separator: str,
    expected_output: Any,
    mock_recipe: MockRecipe,
) -> None:
    step = step_class(
        name=f"test_{step_class.__name__}",
        thousands_separator=thousands_separator,
        decimal_separator=decimal_separator,
    )
    result = step.execute(mock_recipe, input_value)
    assert result == expected_output


@pytest.mark.asyncio
async def test_join_base_url(mock_recipe: MockRecipe) -> None:
    step = JoinBaseUrl(name="test_join_url")
    result = step.execute(mock_recipe, "/get")
    assert result == f"{HTTPBIN_URL}/get"


@pytest.mark.asyncio
async def test_join_base_url_suffix(mock_recipe: MockRecipe) -> None:
    step = JoinBaseUrl(name="test_join_url", suffix="/id")
    result = step.execute(mock_recipe, ["/get", "/hello"])
    assert result == [f"{HTTPBIN_URL}/get/id", f"{HTTPBIN_URL}/hello/id"]
