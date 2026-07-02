import os
import sqlite3
from datetime import datetime, timedelta

# Default cache DB path in user's home folder
DEFAULT_DB_PATH = os.path.expanduser("~/.tz_cli_cache.db")

# Embedded local database for offline fallback (T005)
EMBEDDED_LOCATIONS = {
    # Cities (keys in lowercase)
    "taipei": {
        "display_name": "Taipei, Taiwan",
        "timezone_name": "Asia/Taipei",
        "latitude": 25.0330,
        "longitude": 121.5654
    },
    "tokyo": {
        "display_name": "Tokyo, Japan",
        "timezone_name": "Asia/Tokyo",
        "latitude": 35.6762,
        "longitude": 139.6503
    },
    "london": {
        "display_name": "London, UK",
        "timezone_name": "Europe/London",
        "latitude": 51.5074,
        "longitude": -0.1278
    },
    "new york": {
        "display_name": "New York, USA",
        "timezone_name": "America/New_York",
        "latitude": 40.7128,
        "longitude": -74.0060
    },
    "san francisco": {
        "display_name": "San Francisco, USA",
        "timezone_name": "America/Los_Angeles",
        "latitude": 37.7749,
        "longitude": -122.4194
    },
    "los angeles": {
        "display_name": "Los Angeles, USA",
        "timezone_name": "America/Los_Angeles",
        "latitude": 34.0522,
        "longitude": -118.2437
    },
    "paris": {
        "display_name": "Paris, France",
        "timezone_name": "Europe/Paris",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    "berlin": {
        "display_name": "Berlin, Germany",
        "timezone_name": "Europe/Berlin",
        "latitude": 52.5200,
        "longitude": 13.4050
    },
    "sydney": {
        "display_name": "Sydney, Australia",
        "timezone_name": "Australia/Sydney",
        "latitude": -33.8688,
        "longitude": 151.2093
    },
    "singapore": {
        "display_name": "Singapore, Singapore",
        "timezone_name": "Asia/Singapore",
        "latitude": 1.3521,
        "longitude": 103.8198
    },
    # US Zipcodes
    "10001": {
        "display_name": "New York City, NY, USA (10001)",
        "timezone_name": "America/New_York",
        "latitude": 40.7501,
        "longitude": -73.9996
    },
    "90210": {
        "display_name": "Beverly Hills, CA, USA (90210)",
        "timezone_name": "America/Los_Angeles",
        "latitude": 34.0901,
        "longitude": -118.4065
    },
    "94105": {
        "display_name": "San Francisco, CA, USA (94105)",
        "timezone_name": "America/Los_Angeles",
        "latitude": 37.7884,
        "longitude": -122.3934
    },
    "60601": {
        "display_name": "Chicago, IL, USA (60601)",
        "timezone_name": "America/Chicago",
        "latitude": 41.8858,
        "longitude": -87.6229
    },
    "90001": {
        "display_name": "Los Angeles, CA, USA (90001)",
        "timezone_name": "America/Los_Angeles",
        "latitude": 33.9740,
        "longitude": -118.2497
    }
}


def init_db(db_path=None):
    """Initializes SQLite database and tables."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    
    # Ensure directory exists for cache db
    if db_path != ":memory:":
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geocoding_cache (
        query TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        timezone_name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    return conn


def get_cached_location(query, conn):
    """Gets resolved location from local cache if it exists and is fresh (TTL: 30 days)."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT display_name, timezone_name, latitude, longitude, created_at FROM geocoding_cache WHERE query = ?",
        (query.lower().strip(),)
    )
    row = cursor.fetchone()
    if row:
        display_name, timezone_name, latitude, longitude, created_at_str = row
        try:
            created_at = datetime.fromisoformat(created_at_str)
        except ValueError:
            # Fallback if sqlite date format differs
            created_at = datetime.strptime(created_at_str.split(".")[0], "%Y-%m-%d %H:%M:%S")
            
        if datetime.utcnow() - created_at < timedelta(days=30):
            return {
                "display_name": display_name,
                "timezone_name": timezone_name,
                "latitude": latitude,
                "longitude": longitude,
                "source": "cache"
            }
    return None


def set_cached_location(query, data, conn):
    """Saves geocoding resolution to SQLite cache."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO geocoding_cache (query, display_name, timezone_name, latitude, longitude, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            query.lower().strip(),
            data["display_name"],
            data["timezone_name"],
            data["latitude"],
            data["longitude"],
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
