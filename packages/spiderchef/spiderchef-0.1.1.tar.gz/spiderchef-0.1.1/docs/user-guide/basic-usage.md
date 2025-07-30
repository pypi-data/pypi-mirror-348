# Basic Usage

SpiderChef is designed to be simple to use while providing powerful web scraping capabilities. This guide covers the fundamental patterns for using SpiderChef in your projects.

## Using SpiderChef with YAML Recipes

The most common way to use SpiderChef is by defining your scraping logic in YAML files:

```python
import asyncio
from spiderchef import Recipe

# Import a recipe from a YAML file
recipe = Recipe.from_yaml('recipe_example.yaml')

# Run the recipe
result = asyncio.run(recipe.cook())
print(result)
```

## Using SpiderChef Programmatically

You can also create recipes directly in code:

```python
import asyncio
from spiderchef import Recipe
from spiderchef.steps import FetchStep, RegexStep, JoinBaseUrlStep

# Create a recipe programmatically
recipe = Recipe(
    base_url="https://example.com",
    name="ProductExtractor",
    steps=[
        FetchStep(
            name="fetch_product_page",
            page_type="text",
            path="/products",
            params={
                "category": "electronics",
                "sort": "price_asc"
            }
        ),
        RegexStep(
            name="extract_product_urls",
            expression=r'"(\/product\/[^"]+)"'
        ),
        JoinBaseUrlStep(
            name="format_urls"
        )
    ]
)

# Run the recipe
result = asyncio.run(recipe.cook())
print(result)
```

## Recipe Execution Flow

When you run a recipe with `recipe.cook()`:

1. SpiderChef initializes the recipe context
2. Steps are executed in sequence
3. Each step receives the output of the previous step as input
4. The final step's output is returned as the recipe result

## Command Line Usage

If you've installed SpiderChef with the CLI extras (`pip install spiderchef[cli]`), you can run recipes directly from the command line:

```bash
# Run a recipe
spiderchef cook path/to/recipe.yaml

# Create a new recipe template
spiderchef recipe new my_extraction
```

## Error Handling

SpiderChef provides specific exceptions to help you identify and troubleshoot issues:

```python
from spiderchef.exceptions import SpiderChefError, RecipeError, StepError

try:
    result = asyncio.run(recipe.cook())
except RecipeError as e:
    print(f"Recipe error: {e}")
except StepError as e:
    print(f"Step error: {e}")
except SpiderChefError as e:
    print(f"General error: {e}")
```
