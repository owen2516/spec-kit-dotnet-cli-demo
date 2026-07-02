import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
from src.cache import EMBEDDED_LOCATIONS, get_cached_location, set_cached_location
from src.timezone import resolve_location, get_local_time_details

def test_embedded_location_resolution(temp_db):
    """Verifies that resolve_location retrieves Taipei from local embedded dict."""
    loc = resolve_location("Taipei", temp_db)
    assert loc["display_name"] == "Taipei, Taiwan"
    assert loc["timezone_name"] == "Asia/Taipei"
    assert loc["latitude"] == 25.0330
    assert loc["longitude"] == 121.5654
    assert loc["source"] == "local_embedded"

def test_zipcode_embedded_resolution(temp_db):
    """Verifies that resolve_location retrieves zip code from local embedded dict."""
    loc = resolve_location("90210", temp_db)
    assert loc["display_name"] == "Beverly Hills, CA, USA (90210)"
    assert loc["timezone_name"] == "America/Los_Angeles"
    assert loc["source"] == "local_embedded"

def test_cache_hit(temp_db):
    """Verifies location resolution from cache after setting it."""
    data = {
        "display_name": "Berlin, Germany",
        "timezone_name": "Europe/Berlin",
        "latitude": 52.5200,
        "longitude": 13.4050
    }
    set_cached_location("berlin", data, temp_db)
    
    loc = resolve_location("Berlin", temp_db)
    assert loc["display_name"] == "Berlin, Germany"
    assert loc["source"] == "cache"

def test_timezone_query_format_resolution(temp_db):
    """Verifies that specifying a valid IANA timezone identifier directly works."""
    loc = resolve_location("Europe/Paris", temp_db)
    assert loc["display_name"] == "Europe/Paris"
    assert loc["timezone_name"] == "Europe/Paris"
    assert loc["source"] == "timezone_direct"

def test_get_local_time_details():
    """Verifies timezone current details output format."""
    # Freeze time context
    dt = datetime(2026, 7, 2, 15, 0, 0, tzinfo=ZoneInfo("Asia/Taipei"))
    details = get_local_time_details("Asia/Taipei", now_dt=dt)
    
    assert details["timezone"] == "Asia/Taipei"
    assert details["abbreviation"] == "CST"
    assert details["utc_offset"] == "+08:00"
    assert "2026-07-02 15:00:00" in details["formatted_time"]
