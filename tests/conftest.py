import copy
import os
import sys

import pytest

# make src directory importable so we can pull in app.py
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(root, "src"))

from app import app, activities  # noqa: E402  (import after sys.path manipulation)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory database to its original state before each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
def client():
    """TestClient that can be used in tests."""
    from fastapi.testclient import TestClient

    return TestClient(app)
