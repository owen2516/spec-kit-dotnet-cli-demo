# Research: Timezone Scheduler CLI

This document outlines the technical research, technology choices, and architectural decisions for the Timezone Scheduler CLI.

## Technology Choices & Rationale

### 1. Programming Language: Python 3.11+
* **Decision**: Python 3.11+
* **Rationale**: Python provides excellent built-in libraries for date/time manipulation (`datetime` and `zoneinfo`) and has robust testing frameworks (`pytest`). It is ideal for rapid CLI application development.
* **Alternatives Considered**: Go (compiled, fast, but slightly longer development time for date formatting and geocoding integration).

### 2. Timezone & Datetime Library: `zoneinfo` (Standard Library)
* **Decision**: Standard library `zoneinfo` module.
* **Rationale**: Python 3.9+ introduces `zoneinfo`, which uses the system's IANA timezone database. It is the modern standard, replacing the older and deprecated `pytz` package.
* **Alternatives Considered**: `pytz` (deprecated, has non-standard timezone offsets calculation if instantiated incorrectly), `pendulum` (powerful but adds external dependency).

### 3. Command Line Interface Framework: `click`
* **Decision**: `click` library.
* **Rationale**: `click` is a Python package for creating beautiful command line interfaces in a composable way. It handles arguments, options, types, help page generation, and CLI subcommands automatically.
* **Alternatives Considered**: `argparse` (standard library, but requires verbose boilerplate for nested subcommands), `typer` (modern but adds more dependencies).

### 4. Geocoding & Location Resolution: OpenStreetMap Nominatim API + SQLite Local Cache
* **Decision**: OpenStreetMap Nominatim API for geocoding + local `sqlite3` for query caching.
* **Rationale**: Nominatim provides free geocoding for cities and US zip codes. Since it has a rate limit of 1 request/second and requires a custom User-Agent, we will:
  1. Add a local SQLite cache database to store geocoding results (coordinates and IANA timezone name).
  2. Implement an embedded database containing top 5,000 global cities and US zip codes for offline fallback.
* **Alternatives Considered**: Google Geocoding API (requires paid API keys).

### 5. iCalendar (.ics) File Generation: Built-in Plain Text Generator
* **Decision**: Handcrafted compliant RFC 5545 iCalendar string writer.
* **Rationale**: The iCalendar format for standard single meetings is extremely simple (plain text headers and event lines). Generating this string natively in Python prevents adding external library dependencies (like `icalendar` or `vobject`), maintaining a small footprint.
* **Alternatives Considered**: `icalendar` package (adds overhead and dependencies).

---

## Technical Details & Specifications

### iCalendar (RFC 5545) Format Template
The generated `.ics` file will follow this structure:
```text
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//TimezoneSchedulerCLI//NONSGML v1.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{unique_meeting_id}@tz-cli
DTSTAMP:{utc_now_formatted}
DTSTART:{utc_start_formatted}
DTEND:{utc_end_formatted}
SUMMARY:{meeting_summary}
DESCRIPTION:{meeting_description_with_timezone_details}
LOCATION:{meeting_location_list}
END:VEVENT
END:VCALENDAR
```
All timestamps inside the `.ics` file will be converted to UTC (indicated by the `Z` suffix) to ensure maximum compatibility across Outlook, Google Calendar, and Apple Calendar.

### Calendar Link Generation
Google Calendar quick link format:
`https://calendar.google.com/calendar/render?action=TEMPLATE&text={title}&dates={start_utc}/{end_utc}&details={description}`
Where dates are in `YYYYMMDDTHHMMSSZ` format.
