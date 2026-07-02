# Quickstart Validation Guide: Timezone Scheduler CLI

This document outlines the validation scenarios, prerequisites, and execution commands to verify that the Timezone Scheduler CLI is working end-to-end.

## Prerequisites

1. **Python Version**: Python 3.11+
2. **Dependencies**:
   * `click` (CLI framework)
   * `requests` (Geocoding API requests)
   * `pytest` (Testing)

---

## Setup & Installation

Before running the validation scenarios, set up a virtual environment and install the package:

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies (or install package in editable mode)
pip install click requests pytest
```

---

## Validation Scenarios

### Scenario 1: Location Current Time Query
Verify that querying a location returns the current date, local time, and UTC offset.

* **Command**:
  ```bash
  python -m src.main query "Taipei"
  ```
* **Expected Output**:
  ```text
  Location: Taipei, Taiwan
  Timezone: Asia/Taipei (CST, UTC+08:00)
  Local Time: [Current Date] [Current Time]
  ```

---

### Scenario 2: Datetime Conversion
Verify that converting a source datetime to multiple target destinations outputs the correct local times and day offsets.

* **Command**:
  ```bash
  python -m src.main convert --time "2026-07-02 15:00" --from "Taipei" --to "London" --to "New York"
  ```
* **Expected Output**:
  * Output matches the time differences: London should show `08:00:00` (UTC+1, BST in July), New York should show `03:00:00` (UTC-4, EDT in July).
  * Check the layout matches the ASCII table schema in [cli-contract.md](contracts/cli-contract.md#2-convert).

---

### Scenario 3: Cross-Timezone Meeting Scheduler
Verify that the scheduling algorithm recommends ranked overlapping time windows and successfully exports an ICS file.

* **Command**:
  ```bash
  python -m src.main schedule --locations "Taipei,London,New York" --date "2026-07-03" --duration "1h" --export "meeting.ics"
  ```
* **Expected Output**:
  * A list of ranked suggestions (Rank 1, Rank 2) showing the local meeting hour slots for each location.
  * A Google Calendar quick link matching the formatting in [cli-contract.md](contracts/cli-contract.md#3-schedule).
  * A file `meeting.ics` is generated in the current directory matching the RFC 5545 specifications in [research.md](research.md#icalendar-rfc-5545-format-template).

---

## Running Automated Tests

Verify that all unit and integration tests are passing and meet the coverage requirements defined in the specification.

```bash
# Run tests and output coverage summary
pytest --cov=src tests/
```
