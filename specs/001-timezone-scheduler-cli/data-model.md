# Data Model: Timezone Scheduler CLI

This document specifies the internal data structures and storage schema for the Timezone Scheduler CLI.

## Domain Entities

### 1. Location
Represents a geographic location resolved from a user query (city name, zip code, or IANA timezone string).

| Field Name | Type | Description | Validation / Constraints |
|------------|------|-------------|--------------------------|
| `query` | `str` | Original query string inputted by the user | Case-insensitive |
| `display_name` | `str` | Standardized canonical name | Not empty |
| `timezone_name` | `str` | IANA timezone name (e.g., `Asia/Taipei`) | Must be a valid key in `zoneinfo` |
| `latitude` | `float` | Latitude coordinates | -90.0 to 90.0 |
| `longitude` | `float` | Longitude coordinates | -180.0 to 180.0 |
| `source` | `str` | Data source: `cache`, `local_db`, or `remote_api` | Enforce one of the values |

### 2. LocationTime
Represents the local time and details at a resolved location for a specific UTC timestamp.

| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| `location` | `Location` | The resolved location object | Must not be null |
| `local_time` | `datetime` | Local timezone-aware datetime at this location | Timezone matches `location.timezone_name` |
| `is_business_hours` | `bool` | True if local time falls in the designated meeting range (e.g., 08:00 - 21:00) | Computed property |
| `day_offset` | `int` | Days relative to the meeting's reference date (-1, 0, or +1) | Computed property |

### 3. MeetingProposal
Represents a suggested meeting slot evaluated across multiple locations.

| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| `start_time_utc` | `datetime` | Proposed meeting start time in UTC | Must be in the future |
| `duration_minutes` | `int` | Meeting duration | Positive integer (e.g., 30, 60, 90) |
| `location_times` | `List[LocationTime]` | Local times at all participant locations | Matches total locations query list |
| `score` | `float` | Meeting suitability score (from 0.0 to 1.0) | 0.0 (unusable) to 1.0 (perfect) |

---

## Storage Schema: Local Geocoding Cache

To comply with performance requirements and API rate limits, the tool will store resolved locations in a local SQLite database (`~/.tz_cli_cache.db`).

### Table: `geocoding_cache`

```sql
CREATE TABLE IF NOT EXISTS geocoding_cache (
    query TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    timezone_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Cache Expiry Rule
Geocoding locations rarely change timezones, but IANA database updates can occur. Cached items will have a TTL of 30 days. Queries older than 30 days will be refreshed.
