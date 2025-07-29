from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel

from spiderchef.settings import RE_VAR

if TYPE_CHECKING:
    from spiderchef.recipe import Recipe


class BaseStep(ABC, BaseModel):
    """Base step class that all steps inherit from."""

    name: str = ""
    step_registry: ClassVar[dict[str, type["BaseStep"]]]
    use_previous_output: bool = True

    def _replace(self, variables: dict[str, Any], value: str) -> str:
        """Replaces values if any variables are found."""
        result = value
        for var_name, var_value in variables.items():
            placeholder = f"${{{var_name}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(var_value))

        if "${" in result:
            if unreplaced_var := RE_VAR.findall(result):
                raise ValueError(
                    f"Variable '{unreplaced_var}' not found in Recipe.variables"
                )

        return result

    def _contains_variables(self, structure) -> bool:
        """Check if structure contains any strings with variables."""
        if isinstance(structure, str):
            return "${" in structure
        elif isinstance(structure, dict):
            return any(self._contains_variables(v) for v in structure.values())
        elif isinstance(structure, list):
            return any(self._contains_variables(item) for item in structure)
        return False

    def _replace_in_structure(self, variables: dict[str, Any], structure: Any) -> Any:
        """Replace variables in nested structures."""
        if isinstance(structure, str):
            structure = self._replace(variables, structure)
        elif isinstance(structure, dict):
            structure = {
                k: self._replace_in_structure(variables, v)
                for k, v in structure.items()
            }
        elif isinstance(structure, list):
            structure = [
                self._replace_in_structure(variables, item) for item in structure
            ]
        return structure

    def replace_variables(self, recipe: "Recipe") -> None:
        """Replace variables in all fields of the step."""
        if not recipe.variables:
            return

        for name, field in self:
            if self._contains_variables(field):
                setattr(self, name, self._replace_in_structure(recipe.variables, field))

    @abstractmethod
    def execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        """Execute the step and return the result."""
        self.replace_variables(recipe)


class SyncStep(BaseStep):
    """Base class for synchronous steps."""

    def execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        super().execute(recipe)
        return self._execute(recipe, previous_output)

    @abstractmethod
    def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        """Implementation of the step logic."""
        pass


class AsyncStep(BaseStep):
    """Base class for asynchronous steps."""

    async def execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        super().execute(recipe)
        return await self._execute(recipe, previous_output)

    @abstractmethod
    async def _execute(self, recipe: "Recipe", previous_output: Any = None) -> Any:
        """Implementation of the step logic."""
        pass
