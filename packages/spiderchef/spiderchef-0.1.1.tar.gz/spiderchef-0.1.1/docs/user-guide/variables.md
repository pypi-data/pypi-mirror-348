# Using Variables

SpiderChef provides a powerful variable system that makes your recipes dynamic and reusable. This guide explains how to define, use, and manipulate variables in your recipes.

## Defining Variables

Variables can be defined at the top level of your recipe:

```yaml
name: ProductExtractor
base_url: https://example.com
variables:
  category: electronics
  sort_order: price_asc
  max_pages: 5
```

## Using Variables in Steps

You can reference variables in your steps using the `${variable_name}` syntax:

```yaml
steps:
  - type: fetch
    name: fetch_product_page
    page_type: text
    path: /products
    params:
      category: ${category}
      sort: ${sort_order}
      page: 1
```

## Dynamic Variable Replacement

When running a recipe, you can override default variables:

```python
import asyncio
from spiderchef import Recipe

recipe = Recipe.from_yaml('recipe_example.yaml')

# Override the 'category' variable
result = asyncio.run(recipe.cook(category="books"))
```

This is particularly useful for making your recipes more flexible and reusable.

## Saving Variables During Execution

You can save values as variables during recipe execution using the `save` step:

```yaml
steps:
  - type: xpath
    name: extract_product_title
    expression: //h1[@class='product-title']/text()
  
  - type: save
    name: save_title
    variable: product_title
```

This saves the output of the previous step (the xpath result) as the `product_title` variable, which can then be used in subsequent steps.

## Variable Scope

Variables in SpiderChef have different scopes:

1. **Global variables**: Defined at the recipe level and accessible throughout the recipe
2. **Step output variables**: The output of each step is automatically available to the next step
3. **Saved variables**: Variables saved during execution, accessible in subsequent steps


## Environment Variables

You can access environment variables in your recipes using the `${env.VARIABLE_NAME}` syntax:

```yaml
steps:
  - type: fetch
    name: fetch_api
    url: ${env.API_URL}/products
    headers:
      Authorization: Bearer ${env.API_KEY}
```

This is useful for keeping sensitive information like API keys out of your recipes.
