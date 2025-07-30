# Spider Chef 🕷️👨‍🍳

SpiderChef is a powerful, recipe-based web scraping tool that makes data extraction systematic and reproducible. By defining scraping procedures as "recipes" with sequential "steps," SpiderChef allows you to craft elegant, maintainable data extraction workflows.

```
                   /\
                  /  \
                 |  _ \                   _
                 | / \ \   .--,--        / \
                 |/   \ \  `.  ,.'      /   \
                 /     \ |  |___|  /\  /     \
                /|      \|  ~  ~  /  \/       \
        _______/_|_______\ (o)(o)/___/\_____   \
       /      /  |        (______)     \    \   \_
      /      /   |                      \    \
     /      /    |                       \    \
    /      /     |                        \    \
   /     _/      |                         \    \
  /             _|                          \    \_
_/                                           \_      
```

## Features

- **Recipe-Based Architecture**: Define extraction workflows as YAML recipes
- **Modular Step System**: Build complex scraping logic from reusable components
- **Async Support**: Handle both synchronous and asynchronous extraction steps
- **Type Safety**: Fully typed for better development experience
- **Extensible Design**: Easily create custom steps for specialized extraction needs

## Installation

```bash
# If you want to use the cli
pip install spiderchef[cli]

# If you just want the library usage
pip install spiderchef
```

## Why SpiderChef?

Traditional web scraping often involves writing complex, difficult-to-maintain code that mixes HTTP requests, parsing, and business logic. SpiderChef separates these concerns by:

- Breaking extraction into discrete, reusable steps
- Defining workflows as declarative recipes
- Handling common extraction patterns with built-in steps
- Making scraping procedures reproducible and maintainable

Whether you're scraping product data, monitoring prices, or extracting research information, SpiderChef helps you build structured, reliable data extraction pipelines.
