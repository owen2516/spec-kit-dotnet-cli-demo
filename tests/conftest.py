import pytest
import sqlite3
from src.cache import init_db

@pytest.fixture
def temp_db():
    """Provides an in-memory SQLite database connection with tables initialized."""
    conn = init_db(":memory:")
    yield conn
    conn.close()

@pytest.fixture
def mock_nominatim_success(monkeypatch):
    """Mocks standard Nominatim API HTTP response."""
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self._json = json_data
            self.status_code = status_code
        def json(self):
            return self._json
        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception("API error")

    def mock_get(url, headers=None, timeout=None):
        # Check coordinates query or location queries
        if "q=London" in url:
            return MockResponse([{
                "display_name": "London, Greater London, England, United Kingdom",
                "lat": "51.5074",
                "lon": "-0.1278"
            }])
        elif "lat=51.5074" in url and "lon=-0.1278" in url:
            # Reverse lookup for IANA timezone if applicable or details
            return MockResponse({"timezone": "Europe/London"})
        return MockResponse([], status_code=404)

    # We mock requests.get when imported
    import requests
    monkeypatch.setattr(requests, "get", mock_get)
