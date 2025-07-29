from unittest.mock import MagicMock

import pytest
from tests.conftest import MockRecipe

from spiderchef.steps import STEP_REGISTRY
from spiderchef.steps.extract import (
    ExtractItemsStep,
    GetValueStep,
    RegexFirstStep,
    RegexValueStep,
    XpathFirstStep,
    XpathValueStep,
)


@pytest.mark.parametrize(
    "input_value, expression, expected",
    [
        ({"hello": {"mark": 1}}, r"hello.mark", 1),
        ({"hello": {"mark": [1, 2]}}, r"hello.mark.1", 2),
        (
            {"hello": {"mark": [{"there": "wow"}, {"there": "crazy"}]}},
            r"hello.mark[].there",
            ["wow", "crazy"],
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_value_step(input_value, expression, expected):
    step = GetValueStep(name="test_get", expression=expression)
    result = step.execute(MagicMock(), input_value)
    assert result == expected


@pytest.mark.parametrize(
    "input_value, pattern, expected",
    [
        ("<div>Extract this</div>", r"<div>(.*?)</div>", ["Extract this"]),
        ("No match here", r"pattern", []),
    ],
)
@pytest.mark.asyncio
async def test_regex_value_step(input_value, pattern, expected):
    step = RegexValueStep(name="test_regex", expression=pattern)
    result = step.execute(MagicMock(), input_value)
    assert result == expected


def test_regex_value_step_response(mock_recipe: MockRecipe) -> None:
    step = RegexValueStep(
        name="test_regex", expression=r"<h2>(.*?)</h2>", use_previous_output=False
    )
    result = step.execute(mock_recipe, None)
    assert result == ["Product 1", "Product 2"]


@pytest.mark.parametrize(
    "input_value, pattern, expected",
    [
        ("<div>Extract this</div>", r"<div>(.*?)</div>", "Extract this"),
        ("No match here", r"pattern", []),
    ],
)
@pytest.mark.asyncio
async def test_regex_first_step(input_value, pattern, expected):
    step = RegexFirstStep(name="test_regex_first", expression=pattern)
    result = step.execute(MagicMock(), input_value)
    assert result == expected


@pytest.mark.parametrize(
    "input_html, xpath, return_type, expected",
    [
        (
            "<html><body><div>Item 1</div><div>Item 2</div></body></html>",
            "//div",
            "text",
            ["Item 1", "Item 2"],
        ),
        (
            "<html><body><div>Item 1</div><div>Item 2</div></body></html>",
            "//div/text()",
            "html",
            ["Item 1", "Item 2"],
        ),
        ("<p>No match</p>", "//div", "html", []),
    ],
)
def test_xpath_value_step(input_html, xpath, return_type, expected):
    step = XpathValueStep(name="test_xpath", expression=xpath, return_type=return_type)
    result = step.execute(MagicMock(), input_html)
    assert result == expected


def test_xpath_value_step_response(mock_recipe: MockRecipe) -> None:
    step = XpathValueStep(
        name="test_xpath", expression="//h2/text()", use_previous_output=False
    )
    result = step.execute(mock_recipe, None)
    assert result == ["Product 1", "Product 2"]


@pytest.mark.parametrize(
    "input_html, xpath, expected",
    [
        (
            "<html><body><div>Item 1</div><div>Item 2</div></body></html>",
            "//div/text()",
            "Item 1",
        ),
        ("<p>No match</p>", "//div", []),
    ],
)
@pytest.mark.asyncio
async def test_xpath_first_step(input_html, xpath, expected):
    step = XpathFirstStep(name="test_xpath_first", expression=xpath)
    result = step.execute(MagicMock(), input_html)
    assert result == expected


@pytest.mark.asyncio
async def test_extract_items_step(mock_recipe: MockRecipe):
    html_content = """
    <div class="product">
        <h2>Product 1</h2>
        <p class="price">$10.99</p>
        <script>{"color": "green"}</script>
    </div>
    <div class="product">
        <h2>Product 2</h2>
        <p class="price">$20.50</p>
        <script>{"color": "blue"}</script>
    </div>
    """
    ExtractItemsStep.step_registry = STEP_REGISTRY
    step = ExtractItemsStep(
        name="extract_products",
        expression="//div[@class='product']",
        expression_type="xpath",
        items={
            "title": [{"type": "xpath_first", "expression": ".//h2/text()"}],
            "price": [
                {
                    "type": "xpath_first",
                    "expression": ".//p[@class='price']/text()",
                },
                {
                    "type": "to_money",
                    "decimal_separator": ".",
                    "thousands_seperator": ",",
                },
            ],
            "color": [
                {"type": "xpath_first", "expression": "//script/text()"},
                {"type": "from_json"},
                {"type": "get", "expression": "color"},
            ],
        },
    )

    result = await step.execute(mock_recipe, html_content)
    assert len(result) == 2
    assert result[0]["title"] == "Product 1"
    assert result[0]["price"] == 10.99
    assert result[0]["color"] == "green"

    assert result[1]["title"] == "Product 2"
    assert result[1]["price"] == 20.50
    assert result[1]["color"] == "blue"


@pytest.mark.asyncio
async def test_extract_items_step_regex(mock_recipe: MockRecipe):
    html_content = """
    <div class="product">
        <h2>Product 1</h2>
        <p class="price">$10.99</p>
        <script>{"color": "green"}</script>
    </div>
    <div class="product">
        <h2>Product 2</h2>
        <p class="price">$20.50</p>
        <script>{"color": "blue"}</script>
    </div>
    """
    ExtractItemsStep.step_registry = STEP_REGISTRY
    step = ExtractItemsStep(
        name="extract_products",
        expression="<div[^>]+?>([\s\S]+?)<\/div>",
        expression_type="regex",
        items={
            "title": [{"type": "xpath_first", "expression": ".//h2/text()"}],
            "price": [
                {
                    "type": "xpath_first",
                    "expression": ".//p[@class='price']/text()",
                },
                {
                    "type": "to_money",
                    "decimal_separator": ".",
                    "thousands_seperator": ",",
                },
            ],
            "color": [
                {"type": "xpath_first", "expression": "//script/text()"},
                {"type": "from_json"},
                {"type": "get", "expression": "color"},
            ],
        },
    )

    result = await step.execute(mock_recipe, html_content)
    assert len(result) == 2
    assert result[0]["title"] == "Product 1"
    assert result[0]["price"] == 10.99
    assert result[0]["color"] == "green"

    assert result[1]["title"] == "Product 2"
    assert result[1]["price"] == 20.50
    assert result[1]["color"] == "blue"


@pytest.mark.asyncio
async def test_extract_items_step_json(mock_recipe: MockRecipe):
    json_content = {"items": [{"id": 1}, {"id": 2}, {"id": 3}]}
    ExtractItemsStep.step_registry = STEP_REGISTRY
    step = ExtractItemsStep(
        name="extract_products",
        expression="items",
        expression_type="json",
        items={
            "title": [
                {"type": "get", "expression": "id"},
                {"type": "sleep", "timeout": 0},
            ],
        },
    )

    result = await step.execute(mock_recipe, json_content)
    assert len(result) == 3
    assert result[0]["title"]


@pytest.mark.asyncio
async def test_extract_items_step_json_no_items(mock_recipe: MockRecipe):
    json_content = {"items": [{"id": 1}, {"id": 2}, {"id": 3}]}
    ExtractItemsStep.step_registry = STEP_REGISTRY
    step = ExtractItemsStep(
        name="extract_products",
        expression="items_2",
        expression_type="json",
        items={
            "title": [{"type": "get", "expression": "id"}],
        },
    )

    result = await step.execute(mock_recipe, json_content)
    assert len(result) == 0
