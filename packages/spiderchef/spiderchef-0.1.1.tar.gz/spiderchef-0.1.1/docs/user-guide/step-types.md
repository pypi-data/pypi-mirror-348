# Step Types

SpiderChef comes with a variety of built-in step types to handle common web scraping and data transformation tasks. This guide provides an overview of the available step types, their options, and how to use them.

## Fetching & Asynchronous Steps

### `fetch`
Retrieves content from a URL.

**Options:**
- `name` (str, optional): Step name.
- `page_type` (str, optional): "text", "json", or "binary".
- `path` (str, optional): Relative to base_url.
- `params` (dict, optional): Query parameters.
- `headers` (dict, optional): Custom headers.
- `method` (str, optional): HTTP method (GET, POST, etc.).
- `data` (dict, optional): Data to send in the request body.

```yaml
- type: fetch
  name: fetch_home_page
  page_type: text
  path: /
  params:
    lang: en
  headers:
    User-Agent: "Spider Chef Bot/1.0"
  method: GET
  data: {}
```

### `sleep`
Pauses execution for a specified duration.

**Options:**
- `name` (str, optional): Step name.
- `seconds` (int): Number of seconds to sleep.

```yaml
- type: sleep
  name: pause_between_requests
  timeout: 2
```

## Extraction Steps

### `get`
Extracts a value from a dictionary or list by key or index.

**Options:**
- `name` (str, optional): Step name.
- `key` (str|int): Key or index to extract, supports jmespath like expressions.

```yaml
- type: get
  name: get_field
  key: some_key
```

### `extract_items`
Extracts items from a list or collection.

**Options:**
- `name` (str, optional): Step name.
- `expression` (str): Expression for extraction of items.
- `expression_type` (str): Expression type (e.g. xpath, regex, get)
- `items` (list[Step]): Dictionary of keys and list of steps

```yaml
- type: extract_items
  name: Extracting Items
  expression: items
  expression_type: json
  items:
    url:
      - type: get
        expression: propertyId
      - type: join_base_url
    title:
      - type: get
        expression: agencyReference
```

### `regex`
Extracts data using regular expressions.

**Options:**
- `name` (str, optional): Step name.
- `expression` (str): Regex pattern.

```yaml
- type: regex
  name: extract_links
  expression: 'href="([^"]+)"'
```

### `regex_first`
Extracts the first match using a regular expression.

**Options:**
- `name` (str, optional): Step name.
- `expression` (str): Regex pattern.

```yaml
- type: regex_first
  name: extract_first_link
  expression: 'href="([^"]+)"'
```

### `xpath`
Extracts data using XPath queries.

**Options:**
- `name` (str, optional): Step name.
- `expression` (str): XPath expression.

```yaml
- type: xpath
  name: extract_titles
  expression: //h2[@class='product-title']/text()
```

### `xpath_first`
Extracts the first match using an XPath query.

**Options:**
- `name` (str, optional): Step name.
- `expression` (str): XPath expression.

```yaml
- type: xpath_first
  name: extract_first_title
  expression: //h2[@class='product-title']/text()
```

## Formatting & Transformation Steps

### `from_json`
Parses a JSON string into a Python object.

**Options:**
- `name` (str, optional): Step name.

```yaml
- type: from_json
  name: parse_json
```

### `join_base_url`
Joins relative URLs with the base URL.

**Options:**
- `name` (str, optional): Step name.
- `path` (str, optional): Path to prepend.
- `suffix` (str, optional): Suffix to append.


```yaml
- type: join_base_url
  name: format_urls
  path: /es/alquiler/vivienda/-/-/
  suffix: /d
```

### `remove_extra_whitespace`
Removes extra whitespace from a string.

**Options:**
- `name` (str, optional): Step name.

```yaml
- type: remove_extra_whitespace
  name: clean_whitespace
```

### `remove_html_tags`
Removes HTML tags from a string.

**Options:**
- `name` (str, optional): Step name.

```yaml
- type: remove_html_tags
  name: strip_html
```

### `to_money`
Converts a string to a money/decimal value.

**Options:**
- `name` (str, optional): Step name.

```yaml
- type: to_money
  name: convert_to_money
```

### `to_int`
Converts a value to an integer.

**Options:**
- `name` (str, optional): Step name.

```yaml
- type: to_int
  name: convert_to_int
```

### `to_str`
Converts a value to a string.

**Options:**
- `name` (str, optional): Step name.

```yaml
- type: to_str
  name: convert_to_str
```

### `to_float`
Converts a value to a float.

**Options:**
- `name` (str, optional): Step name.

```yaml
- type: to_float
  name: convert_to_float
```

## Data Management Steps

### `save`
Saves data to a variable.

**Options:**
- `name` (str, optional): Step name.
- `variable` (str): Variable name to save to.

```yaml
- type: save
  name: save_title
  variable: title
```

## Conditional & Error Handling Steps

### `compare`
Compares values for conditional logic.

**Options:**
- `name` (str, optional): Step name.
- `left` (any): Left value.
- `op` (str): Operator (e.g., eq, ne, gt, lt).
- `right` (any): Right value.

```yaml
- type: compare
  name: check_value
  left: ${some_var}
  op: eq
  right: 42
```

### `try_catch`
Handles errors in a sequence of steps.

**Options:**
- `name` (str, optional): Step name.
- `try` (list[Step]): Steps to try.
- `catch` (list[Step]): Steps to run on error.

```yaml
- type: try_catch
  name: try_fetch
  try:
    - type: fetch
      # ...
  catch:
    - type: save
      # ...
```

---

You can also create [custom steps](../advanced/custom-steps.md) for specialized extraction needs.
