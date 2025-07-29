import asyncio
from typing import Any

from spiderchef import AsyncStep


async def test_smoke_spiderchef() -> None:
    """Smoke test for spiderchef initialization and class usage."""
    try:
        from spiderchef import STEP_REGISTRY, Recipe, SyncStep

        class HelloStep(SyncStep):
            person_name: str

            def _execute(self, recipe: Recipe, previous_output: Any = None) -> str:
                return f"Hello There {self.person_name}"

        class SleepStep(AsyncStep):
            async def _execute(
                self, recipe: Recipe, previous_output: Any = None
            ) -> Any:
                await asyncio.sleep(0)
                return previous_output

        CUSTOM_STEP_REGISTRY = {**STEP_REGISTRY, "hello": HelloStep, "sleep": SleepStep}

        # Overrides the global step registry with your own
        Recipe.step_registry = CUSTOM_STEP_REGISTRY

        # You can manually initiziales a recipe like so, or just use the yaml recipe.
        recipe = Recipe(
            base_url="https://example.com",
            name="Example",
            steps=[
                HelloStep(name="Saying Hello", person_name="George"),
                SleepStep(name="Sleeping"),
            ],
        )
        await recipe.cook()
    except Exception as e:
        raise RuntimeError("SpiderChef smoke test failed") from e


async def main() -> None:
    await test_smoke_spiderchef()


if __name__ == "__main__":
    asyncio.run(main())
    print("Smoke tests completed successfully.")
