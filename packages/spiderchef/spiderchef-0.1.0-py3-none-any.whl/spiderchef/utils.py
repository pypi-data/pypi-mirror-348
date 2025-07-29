from __future__ import annotations

from typing import Any

from spiderchef.steps import BaseStep


def convert_steps(step_registry: dict[str, Any], value: list[dict]) -> list[BaseStep]:
    """Convert step dictionaries to Step instances before model creation."""
    converted_steps = []
    for step in value:
        if isinstance(step, dict) and "type" in step:
            step_class = step_registry.get(step["type"])
            if not step_class:
                raise ValueError(f"Unknown step type: {step['type']}")

            step_class.step_registry = step_registry
            # Create the step instance
            step_instance = step_class(**step)

            converted_steps.append(step_instance)
        else:
            # If it's already a Step instance or something else, keep it as is
            converted_steps.append(step)

    return converted_steps
