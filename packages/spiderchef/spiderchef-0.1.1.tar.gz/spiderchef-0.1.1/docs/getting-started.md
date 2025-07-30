# Getting Started with SpiderChef

This guide will help you get up and running with SpiderChef quickly. We'll cover installation, basic usage, and a simple example to demonstrate how SpiderChef works.

## Installation

SpiderChef can be installed using pip:

```bash
# For CLI usage
pip install spiderchef[cli]

# For library usage only
pip install spiderchef
```

## CLI Usage

SpiderChef comes with a command-line interface that makes it easy to run recipes:

```bash
# Run a recipe
spiderchef cook recipes/example.yaml

# Create a new recipe template
spiderchef recipe new my_extraction
```

## Basic Library Usage

Here's a simple example of using SpiderChef in your Python code:

```python
import asyncio
from spiderchef import Recipe

# Import a recipe from a YAML file
recipe = Recipe.from_yaml('recipe_example.yaml')

# Run the recipe
asyncio.run(recipe.cook())
```

## Your First Recipe

Here's a basic recipe example that fetches a webpage and extracts information:

```yaml
base_url: https://example.com
name: ProductExtractor
steps:
  - type: fetch
    name: fetch_product_page
    page_type: text
    path: /products
    params:
      category: electronics
      sort: price_asc
  
  - type: regex
    name: extract_product_urls
    expression: '"(\/product\/[^"]+)"'
  
  - type: join_base_url
    name: format_urls
```

This recipe:

1. Fetches the product listing page
2. Extracts product URLs using a regex pattern
3. Joins the extracted URLs with the base URL

## Next Steps

Now that you have a basic understanding of SpiderChef, you can:

- Learn about the [Recipe Format](user-guide/recipe-format.md)
- Explore available [Step Types](user-guide/step-types.md)
- Discover how to use [Variables](user-guide/variables.md) in your recipes
- Create [Custom Steps](advanced/custom-steps.md) for specialized extraction needs
