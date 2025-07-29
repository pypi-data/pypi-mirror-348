from __future__ import annotations

import string
from re import findall
from typing import TYPE_CHECKING, Any, Literal

from lxml.html import fromstring, tostring
from pydantic import field_validator
from pydash import get
from structlog import get_logger

from spiderchef.steps.base import AsyncStep, BaseStep, SyncStep
from spiderchef.utils import convert_steps

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe

log = get_logger()


class GetValueStep(SyncStep):
    """Step to get a value from the recipe's JSON data."""

    expression: str

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        if "[]" in self.expression:
            expr = self.expression.replace("[]", "")
            json_value = (
                previous_output if self.use_previous_output else recipe.json_response
            )
            for i in expr.split("."):
                if isinstance(json_value, dict):
                    json_value = get(json_value, i)
                elif isinstance(json_value, list):
                    json_value = [get(val, i) for val in json_value]
            return json_value
        return get(
            previous_output if self.use_previous_output else recipe.json_response,
            self.expression,
        )


class XpathValueStep(SyncStep):
    """Step to xpath a value from the recipe's text data."""

    expression: str
    return_type: Literal["text", "html"] = "html"
    rebuild_tree: bool = False
    index: int | None = None

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        tree = None
        output = []
        if not self.use_previous_output and not recipe._tree or self.rebuild_tree:
            recipe._tree = tree = fromstring(recipe.text_response)
        if self.use_previous_output and isinstance(previous_output, str):
            tree = fromstring(previous_output)
        if tree is not None:
            for i in tree.xpath(self.expression):
                if isinstance(i, str):
                    output.append(i)
                elif self.return_type == "text":
                    output.append("".join(i.itertext()))
                else:
                    item = tostring(i, encoding="utf-8")
                    output.append(item.decode() if isinstance(item, bytes) else item)
        if isinstance(self.index, int) and output and len(output) >= self.index:
            return output[self.index]
        return output


class XpathFirstStep(XpathValueStep):
    index: int | None = 0


class RegexValueStep(SyncStep):
    """Step to regex a value from the recipe's text data."""

    index: int | None = None
    expression: str

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        items = []
        if not self.use_previous_output and recipe.text_response:
            items = findall(self.expression, recipe.text_response)
        else:
            items = findall(self.expression, previous_output)
        if isinstance(self.index, int) and items and len(items) >= self.index:
            return items[self.index]
        return items


class RegexFirstStep(RegexValueStep):
    index: int | None = 0


class ExtractItemsStep(AsyncStep):
    """Step to regex a value from the recipe's text data."""

    expression: str
    expression_type: Literal["json", "xpath", "regex"] = "regex"
    items: dict[str, list[BaseStep]]

    @field_validator("items", mode="before")
    def convert_step_dicts(
        cls, value: dict[str, list[dict]]
    ) -> dict[str, list[BaseStep]]:
        """Convert step dictionaries to Step instances before model creation."""
        converted_steps = {}
        for item, steps in value.items():
            converted_steps[item] = convert_steps(cls.step_registry, steps)

        return converted_steps

    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        outputs = []
        match self.expression_type:
            case "json":
                extraction_cls = GetValueStep
            case "xpath":
                extraction_cls = XpathValueStep
            case "regex":
                extraction_cls = RegexValueStep

        data_items = extraction_cls(
            expression=self.expression,
            use_previous_output=self.use_previous_output,
        ).execute(recipe, previous_output)
        if not data_items:
            return []
        for data_number, data in enumerate(data_items, start=1):
            output = {}
            log.info(f"  ➡️  {data_number}.  Extracting item ")
            for item_number, item in zip(string.ascii_lowercase, self.items.items()):
                item, steps = item
                item_output = data
                log.info(f"    ➡️  {item_number}.  Extracting {item}...")
                for step in steps:
                    if issubclass(type(step), AsyncStep):
                        item_output = await step.execute(recipe, item_output)
                    else:
                        item_output = step.execute(recipe, item_output)
                output[item] = item_output
            outputs.append(output)
        return outputs
