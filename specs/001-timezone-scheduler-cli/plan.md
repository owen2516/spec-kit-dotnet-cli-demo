# Implementation Plan: Timezone Scheduler CLI

**Branch**: `001-timezone-scheduler-cli` | **Date**: 2026-07-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-timezone-scheduler-cli/spec.md`

**Note**: This plan defines the implementation steps and architecture decisions for the Timezone Scheduler CLI.

## Summary

The Timezone Scheduler CLI is a Python command line application that allows users to query current date/time by location names, timezones, or US zip codes. It provides subcommands for datetime conversion across multiple destinations and recommends optimal meeting times for participants distributed across different timezones by maximizing reasonable local overlap hours. Results can be exported directly as RFC-compliant `.ics` files and Google Calendar quick links.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `click` (CLI framework), `requests` (Geocoding HTTP queries)

**Storage**: `sqlite3` (built-in cache schema with a local database file at `~/.tz_cli_cache.db`)

**Testing**: `pytest`, `pytest-cov`, `pytest-mock` (target code coverage >= 80%)

**Target Platform**: Cross-platform (Windows, macOS, Linux)

**Project Type**: CLI utility

**Performance Goals**: Local timezone calculations < 50ms, geocoding remote API queries with cache hit < 10ms, cache miss < 1000ms.

**Constraints**: Maximize local cache usage to satisfy rate-limiting criteria of free Nominatim geocoding API. Provide embedded fallback data.

**Scale/Scope**: Local execution per user.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Code Quality Check**: The design utilizes a modular structure (separating CLI presentation, scheduling logic, and caching layers) and follows clean code guidelines without over-engineering.
- [x] **Testing Standards Check**: Automated unit and integration tests are mandatory and will be built using `pytest` to target >= 80% coverage.
- [x] **UX Consistency Check**: Subcommands, flags, and parameters follow the Click CLI standard guidelines. Exit codes and error formats are standardized (0 for success, 1 for argument error, 2 for resolution/API error).
- [x] **Performance Requirements Check**: SQLite caching ensures all repeated location queries avoid slow geocoding API calls, ensuring execution well within the performance limit.

## Project Structure

### Documentation (this feature)

```text
specs/001-timezone-scheduler-cli/
├── plan.md              # This file
├── research.md          # Technology choices and ICS specification
├── data-model.md        # Location, Time, and Proposal entities
├── quickstart.md        # End-to-end validation scenarios
├── contracts/
│   └── cli-contract.md  # CLI arguments and output formats
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py          # Click CLI Entrypoint & subcommand routing
├── cache.py         # SQLite cache layer & embedded geo data resolver
├── timezone.py      # zoneinfo resolver and datetime converter
├── scheduler.py     # Meeting overlap algorithm
└── exporter.py      # iCalendar (.ics) and calendar link builder

tests/
├── __init__.py
├── test_cache.py      # Cache database tests and Mock Nominatim API
├── test_timezone.py   # Datetime conversion and DST transition tests
├── test_scheduler.py  # Meeting recommendation overlap tests
└── test_exporter.py   # ICS validation tests
```

**Structure Decision**: Option 1 (Single Python project layout at repository root).

## Complexity Tracking

*No constitution violations have been identified. The architecture keeps dependencies minimal and utilizes built-in libraries (`zoneinfo`, `sqlite3`) wherever possible.*
