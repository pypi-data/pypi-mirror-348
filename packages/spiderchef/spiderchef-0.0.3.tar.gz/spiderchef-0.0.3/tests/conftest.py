import os
from unittest.mock import MagicMock

import pytest

from spiderchef.steps import STEP_REGISTRY

HTTPBIN_URL = os.environ.get("HTTPBIN_URL", "http://localhost:8000")


class MockRecipe:
    """Mock Recipe for testing steps individually"""

    step_registry = STEP_REGISTRY

    def __init__(self):
        self.base_url = HTTPBIN_URL
        self._session = None
        self._tree = None
        self.json_response = {"hello": 3, "there": 5}
        self.text_response = """
    <div class="product">
        <h2>Product 1</h2>
        <p class="price">$10.99</p>
    </div>
    <div class="product">
        <h2>Product 2</h2>
        <p class="price">$20.50</p>
    </div>"""

    @property
    async def session(self):
        return MagicMock()

    async def close(self):
        pass


@pytest.fixture
def mock_recipe():
    return MockRecipe()
