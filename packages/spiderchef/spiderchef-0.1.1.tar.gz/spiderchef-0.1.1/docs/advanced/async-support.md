# Async Support

SpiderChef is built from the ground up with asynchronous programming support, allowing for efficient handling of I/O-bound operations like web requests. This guide explains how to use SpiderChef's async capabilities.

## Async Execution Model

SpiderChef uses Python's `asyncio` framework for asynchronous execution. When you call `recipe.cook()`, it returns a coroutine that must be executed in an async context:

```python
import asyncio
from spiderchef import Recipe

recipe = Recipe.from_yaml('recipe.yaml')

# Run the recipe asynchronously
result = asyncio.run(recipe.cook())
```

## AsyncStep vs SyncStep

SpiderChef provides two base classes for creating steps:

1. `SyncStep`: For synchronous operations
2. `AsyncStep`: For asynchronous operations that use `await`

### When to Use AsyncStep

Use `AsyncStep` when your step needs to:

- Make HTTP requests
- Query databases asynchronously
- Perform any I/O-bound operations
- Use other async functions or libraries

Here's an example of an `AsyncStep`:

```python
import asyncio
from spiderchef import AsyncStep, Recipe
from typing import Any

class DelayedProcessStep(AsyncStep):
    delay_seconds: int = 1
    
    async def _execute(self, recipe: Recipe, previous_output: Any = None) -> Any:
        # Simulate some async processing
        await asyncio.sleep(self.delay_seconds)
        
        # Process the data
        if isinstance(previous_output, list):
            return [item.upper() if isinstance(item, str) else item 
                    for item in previous_output]
        elif isinstance(previous_output, str):
            return previous_output.upper()
        return previous_output
```

### When to Use SyncStep

Use `SyncStep` for CPU-bound operations or operations that don't benefit from asynchronous execution:

- Data transformation
- Regular expression matching
- Mathematical calculations
- Any processing that doesn't involve waiting for external resources

Here's an example of a `SyncStep`:

```python
from spiderchef import SyncStep, Recipe
from typing import Any

class FilterStep(SyncStep):
    min_length: int = 5
    
    def _execute(self, recipe: Recipe, previous_output: Any = None) -> list:
        if not isinstance(previous_output, list):
            return previous_output
            
        return [item for item in previous_output 
                if isinstance(item, str) and len(item) >= self.min_length]
```

## Mixing Sync and Async Steps

SpiderChef seamlessly handles the mixing of synchronous and asynchronous steps in a recipe. When an async step follows a sync step (or vice versa), SpiderChef handles the transition automatically.

## Parallel Execution

For advanced use cases, you can create steps that execute operations in parallel:

```python
import asyncio
from spiderchef import AsyncStep, Recipe
from typing import Any, List

class ParallelFetchStep(AsyncStep):
    urls: List[str]
    
    async def _execute(self, recipe: Recipe, previous_output: Any = None) -> List[str]:
        async def fetch_url(url):
            # This would use a proper HTTP client in real code
            await asyncio.sleep(1)  # Simulate network delay
            return f"Content from {url}"
            
        # Create tasks for all URLs
        tasks = [fetch_url(url) for url in self.urls]
        
        # Execute all tasks in parallel and wait for them to complete
        results = await asyncio.gather(*tasks)
        
        return results
```

## Best Practices for Async Steps

1. **Use the right base class**: Choose `AsyncStep` for I/O-bound operations and `SyncStep` for CPU-bound operations.

2. **Avoid blocking calls**: Inside an `AsyncStep`, avoid blocking operations that would prevent other tasks from running.

3. **Handle exceptions properly**: Use try/except blocks to properly handle exceptions in asynchronous code.

4. **Consider rate limiting**: When making multiple requests, consider implementing rate limiting to avoid overwhelming the target server.

5. **Use timeouts**: Always set timeouts for network operations to prevent infinite waiting.

## Example: Asynchronous Web Scraper

Here's a complete example of a recipe that uses async steps to scrape multiple pages in parallel:

```yaml
name: ParallelScraper
base_url: https://example.com
steps:
  - type: fetch
    name: fetch_category_page
    page_type: text
    path: /categories
    
  - type: xpath
    name: extract_category_urls
    expression: //a[@class='category-link']/@href
    
  - type: parallel_fetch
    name: fetch_all_categories
    urls: ${previous_output}
    
  - type: foreach
    name: extract_products_from_categories
    steps:
      - type: xpath
        name: extract_product_names
        expression: //div[@class='product']/h3/text()
      
      - type: save
        name: save_category_products
        variable: category_products
```

This recipe:

1. Fetches the main category page
2. Extracts all category URLs
3. Fetches all category pages in parallel
4. For each category page, extracts the product names
5. Saves the products for each category

The `parallel_fetch` step would be a custom async step as shown in the `ParallelFetchStep` example above.
