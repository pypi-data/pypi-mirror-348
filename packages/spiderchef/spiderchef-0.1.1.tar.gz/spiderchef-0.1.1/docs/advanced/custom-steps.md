# Creating Custom Steps

SpiderChef's extensibility comes from its ability to define custom steps. This guide shows you how to create your own steps for specialized extraction needs.

## Step Types

SpiderChef provides two base classes for creating custom steps:

- `SyncStep`: For synchronous operations
- `AsyncStep`: For asynchronous operations

## Creating a Basic Synchronous Step

Here's how to create a simple synchronous step:

```python
from spiderchef import SyncStep, Recipe
from typing import Any

class HelloStep(SyncStep):
    # Step parameters (become constructor arguments)
    person_name: str
    
    def _execute(self, recipe: Recipe, previous_output: Any = None) -> str:
        """Execute the step logic."""
        return f"Hello there, {self.person_name}!"
```

## Creating an Asynchronous Step

For operations that require asynchronous execution, use `AsyncStep`:

```python
import asyncio
from spiderchef import AsyncStep, Recipe
from typing import Any

class SleepStep(AsyncStep):
    sleep_time: int = 5  # Default value
    
    async def _execute(self, recipe: Recipe, previous_output: Any = None) -> Any:
        """Execute the asynchronous step logic."""
        await asyncio.sleep(self.sleep_time)
        return previous_output  # Pass through the previous output
```

## Registering Custom Steps

To use your custom steps in recipes, you need to register them with the step registry:

```python
from spiderchef import STEP_REGISTRY, Recipe

# Create a custom step registry
CUSTOM_STEP_REGISTRY = {
    **STEP_REGISTRY,  # Include all built-in steps
    "hello": HelloStep,
    "sleep": SleepStep
}

# Set the custom registry for your recipes
Recipe.step_registry = CUSTOM_STEP_REGISTRY
```

## Using Custom Steps in YAML Recipes

Once registered, you can use your custom steps in YAML recipes:

```yaml
name: CustomStepExample
base_url: https://example.com
steps:
  - type: hello
    name: greeting
    person_name: Alice
    
  - type: sleep
    name: pause
    sleep_time: 2
```

## Using Custom Steps Programmatically

You can also use custom steps when creating recipes programmatically:

```python
from spiderchef import Recipe

recipe = Recipe(
    base_url="https://example.com",
    name="Example",
    steps=[
        HelloStep(name="Saying Hello", person_name="George"),
        SleepStep(name="Sleeping", sleep_time=3),
    ],
)

# Run the recipe
asyncio.run(recipe.cook())
```

## Advanced Step Features

### Handling Previous Output

Steps receive the output of the previous step, allowing you to chain operations:

```python
class TransformStep(SyncStep):
    transform_type: str = "uppercase"
    
    def _execute(self, recipe: Recipe, previous_output: Any = None) -> Any:
        if not isinstance(previous_output, str):
            return previous_output
            
        if self.transform_type == "uppercase":
            return previous_output.upper()
        elif self.transform_type == "lowercase":
            return previous_output.lower()
        return previous_output
```

### Accessing Recipe Variables

Steps can access recipe variables:

```python
class GreetingStep(SyncStep):
    def _execute(self, recipe: Recipe, previous_output: Any = None) -> str:
        user_name = recipe.variables.get("user_name", "Guest")
        return f"Hello, {user_name}!"
```

### Error Handling

Implement robust error handling in your steps:

```python
from spiderchef.exceptions import StepError

class DivideStep(SyncStep):
    divisor: int
    
    def _execute(self, recipe: Recipe, previous_output: Any = None) -> float:
        try:
            numerator = float(previous_output)
            if self.divisor == 0:
                raise ValueError("Cannot divide by zero")
            return numerator / self.divisor
        except (ValueError, TypeError) as e:
            raise StepError(f"Division error: {str(e)}")
```

## Complete Example

Here's a complete example showing how to create and use custom steps:

```python
import asyncio
from typing import Any, Dict, List, Optional

from spiderchef import STEP_REGISTRY, AsyncStep, Recipe, SyncStep


# Define custom steps
class HelloStep(SyncStep):
    person_name: str

    def _execute(self, recipe: Recipe, previous_output: Any = None) -> str:
        return f"Hello there, {self.person_name}!"


class SleepStep(AsyncStep):
    sleep_time: int = 5

    async def _execute(self, recipe: Recipe, previous_output: Any = None) -> Any:
        await asyncio.sleep(self.sleep_time)
        return previous_output


# Register custom steps
CUSTOM_STEP_REGISTRY = {**STEP_REGISTRY, "hello": HelloStep, "sleep": SleepStep}
Recipe.step_registry = CUSTOM_STEP_REGISTRY

# Create a recipe using custom steps
recipe = Recipe(
    base_url="https://example.com",
    name="Example",
    steps=[
        HelloStep(name="Saying Hello", person_name="George"),
        SleepStep(name="Sleeping", sleep_time=3),
    ],
)

# Run the recipe
result = asyncio.run(recipe.cook())
print(result)
```
