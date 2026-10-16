from collections.abc import Iterator

import pytest

from casehandlersf import api

API_KEY = "test-key-0123456789abcdef0123456789abcdef"
AUTH = {"X-API-Key": API_KEY}


@pytest.fixture(autouse=True)
def api_key(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    """Configure a known API key, ignoring any API_KEY in .env or the environment."""
    monkeypatch.setenv("API_KEY", API_KEY)
    api._api_key.cache_clear()
    yield API_KEY
    api._api_key.cache_clear()
