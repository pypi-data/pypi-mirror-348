from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import field_validator
from structlog import get_logger

from spiderchef.steps.base import AsyncStep, BaseStep
from spiderchef.utils import convert_steps

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe

log = get_logger()


class TryCatchStep(AsyncStep):
    """Execute steps with error handling."""

    try_steps: list[BaseStep]
    catch_steps: list[BaseStep] = []
    finally_steps: list[BaseStep] = []

    @field_validator("try_steps", "catch_steps", "finally_steps", mode="before")
    def convert_steps(cls, value: list[dict[str, Any]]) -> list[BaseStep]:
        """Convert step dictionaries to Step instances before model creation."""
        return convert_steps(cls.step_registry, value)

    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        result = previous_output

        try:
            for step in self.try_steps:
                result = step.execute(recipe, result)
        except Exception as e:
            # Save error in variables for catch steps
            recipe.variables["error"] = str(e)
            recipe.variables["error_type"] = e.__class__.__name__
            log.error(f"{str(e)} caught!", error_type=e.__class__.__name__)
            # Execute catch steps
            catch_result = previous_output
            for step in self.catch_steps:
                catch_result = step.execute(recipe, catch_result)
            result = catch_result

        finally:
            # Execute finally steps
            finally_result = result
            for step in self.finally_steps:
                finally_result = step.execute(recipe, finally_result)
            result = finally_result

        return result
