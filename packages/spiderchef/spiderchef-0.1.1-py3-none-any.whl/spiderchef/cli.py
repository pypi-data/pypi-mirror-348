from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated

import yaml
from structlog import get_logger
from typer import Argument, Option, Typer

from spiderchef.recipe import Recipe
from spiderchef.settings import BASE_RECIPE, HELP

log = get_logger()
app = Typer(name="spiderchef", help=HELP, rich_markup_mode="rich", no_args_is_help=True)
recipe_app = Typer(help="Create and validate new recipes.")
app.add_typer(recipe_app, name="recipe")


@app.command()
def cook(
    recipe_file: str = Argument(..., help="Path to the YAML recipe file"),
    output_file: Annotated[
        str, Option(help="Last name of person to greet.")
    ] = "output.yaml",
):
    """Read the YAML recipe file and perform scraping based on its content."""
    try:
        recipe = Recipe.from_yaml(recipe_file)

        output = asyncio.run(recipe.cook())
        with open(output_file, "w") as f:
            yaml.dump(output, f, encoding=recipe.default_encoding, allow_unicode=True)
    except Exception as e:
        log.exception(f"An error occurred: {e}")


@recipe_app.command()
def new(
    output_file: Path = Option(
        "./config_test.yaml",
        "--output-file",
        "-o",
        help="Path where to save the new recipe file",
        writable=True,
        resolve_path=True,
    ),
):
    """Generate a new recipe config file."""
    with output_file.open("w") as f:
        yaml.dump(BASE_RECIPE, f)


@recipe_app.command()
def validate(recipe_file: str = Argument(..., help="Path to the YAML recipe file")):
    """Validate an existing recipe file."""
    # Just try to load the recipe and see if everything works.
    Recipe.from_yaml(recipe_file)


if __name__ == "__main__":
    app()
