from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydash import get

from spiderchef.steps.base import SyncStep

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe


class CompareStep(SyncStep):
    """Step to compare two values from the recipe's JSON data."""

    left_key: str | None = None
    right_key: str | None = None
    compare_to: Any = None
    condition: Literal[
        "gt",
        "lt",
        "eq",
        "gte",
        "lte",
    ]

    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> bool:
        def get_value(json_response: dict[str, Any], key: str) -> float:
            if value := get(json_response, key):
                return value if isinstance(value, float | int) else len(value)
            raise ValueError(f"Could not get value for key: {key}")

        right_value = None
        if self.use_previous_output:
            json_response = previous_output
        else:
            json_response = recipe.json_response

        if self.left_key is not None:
            left_value = get_value(json_response, self.left_key)
        else:
            left_value = previous_output
        if self.right_key is not None:
            right_value = get_value(json_response, self.right_key)
        elif self.compare_to is not None:
            right_value = self.compare_to

        # Ensure both values are not None before comparison
        if right_value is None or left_value is None:  # pragma: no cover
            raise ValueError(
                f"Cannot compare: left value ({left_value}) or right value ({right_value}) is None"
            )

        match self.condition:
            case "eq":
                return left_value == right_value
            case "gt":
                return left_value > right_value
            case "lt":
                return left_value < right_value
            case "gte":
                return left_value >= right_value
            case "lte":
                return left_value <= right_value
            case _:  # pragma: no cover
                raise ValueError(f"Unknown condition: {self.condition}")
