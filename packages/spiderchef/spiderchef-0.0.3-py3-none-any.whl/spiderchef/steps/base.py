from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe


class BaseStep(ABC, BaseModel):
    """Base step class that all steps inherit from."""

    name: str = "unnamed_step"
    step_registry: ClassVar[dict[str, type["BaseStep"]]]
    use_previous_output: bool = True

    @abstractmethod
    def execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        """Execute the step and return the result."""
        pass


class SyncStep(BaseStep):
    """Base class for synchronous steps."""

    def execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        return self._execute(recipe, previous_output)

    @abstractmethod
    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        """Implementation of the step logic."""
        pass


class AsyncStep(BaseStep):
    """Base class for asynchronous steps."""

    async def execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        return await self._execute(recipe, previous_output)

    @abstractmethod
    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        """Implementation of the step logic."""
        pass
