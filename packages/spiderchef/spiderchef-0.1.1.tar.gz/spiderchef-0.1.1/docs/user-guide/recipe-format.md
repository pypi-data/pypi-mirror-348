# Recipe Format

SpiderChef recipes are defined in YAML format, providing a clear, readable structure for your web scraping workflows. This guide explains the recipe format in detail.

## Basic Recipe Structure

A SpiderChef recipe has the following basic structure:

```yaml
name: MyRecipe
base_url: https://example.com
variables:
  key1: value1
  key2: value2
steps:
  - type: step_type
    name: step_name
    # step-specific parameters
  - type: another_step_type
    name: another_step_name
    # step-specific parameters
```

## Recipe Components

### Name

The `name` field is required and provides a human-readable identifier for your recipe:

```yaml
name: ProductScraper
```

### Base URL

The `base_url` field defines the root URL that the recipe will work with:

```yaml
base_url: https://example.com
```

This is particularly useful when working with relative URLs in your scraping logic.

### Variables

The `variables` section lets you define values that can be reused throughout your recipe:

```yaml
variables:
  category: electronics
  sort_order: price_asc
  max_pages: 5
```

These variables can be referenced in your steps using the `${variable_name}` syntax.

### Steps

The `steps` section is the heart of your recipe, defining the sequence of operations to perform:

```yaml
steps:
  - type: fetch
    name: fetch_product_page
    page_type: text
    path: /products
    params:
      category: ${category}
      sort: ${sort_order}
  
  - type: regex
    name: extract_product_urls
    expression: '"(\/product\/[^"]+)"'
  
  - type: join_base_url
    name: format_urls
```

Each step has:

- A `type` that determines the operation to perform
- A `name` that provides a human-readable identifier
- Additional parameters specific to the step type

## Step Execution Flow

Steps are executed in sequence, with each step receiving the output of the previous step as input. The final step's output becomes the recipe's result.

## Example Recipe

Here's a complete example of a recipe that extracts product information:

```yaml
name: ProductExtractor
base_url: https://example.com
variables:
  category: electronics
  sort_order: price_asc
steps:
  - type: fetch
    name: fetch_product_page
    page_type: text
    path: /products
    params:
      category: ${category}
      sort: ${sort_order}
  
  - type: regex
    name: extract_product_urls
    expression: '"(\/product\/[^"]+)"'
  
  - type: join_base_url
    name: format_urls
    
  - type: foreach
    name: fetch_product_details
    steps:
      - type: fetch
        name: fetch_product_page
        page_type: text
        path: ${item}
      
      - type: xpath
        name: extract_product_title
        expression: //h1[@class='product-title']/text()
        
      - type: xpath
        name: extract_product_price
        expression: //span[@class='price']/text()
        
      - type: save
        variable: product_info
        mapping:
          url: ${item}
          title: ${xpath_result}
          price: ${xpath_result}
```

This recipe:

1. Fetches the product listing page
2. Extracts product URLs using a regex pattern
3. Joins the extracted URLs with the base URL
4. For each URL, fetches the product details page
5. Extracts the product title and price
6. Saves the product information to a variable
