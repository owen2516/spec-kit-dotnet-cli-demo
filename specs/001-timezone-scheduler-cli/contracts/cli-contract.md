# CLI Interface Contract: Timezone Scheduler CLI

This document defines the CLI command schema, input arguments, option flags, output formats, and exit codes for the Timezone Scheduler CLI.

## Command Syntax

The entry command for the tool is `tz-cli`. It supports three primary subcommands: `query`, `convert`, and `schedule`.

---

### 1. `query`
Queries the current date and time of a specific location.

#### CLI Command Schema
```bash
tz-cli query <location> [options]
```

#### Arguments & Options
* `<location>` (Argument, Required): The query string. Can be IANA timezone name (`Asia/Taipei`), city name (`Tokyo`), or US zip code (`94105`).
* `-f, --format <format>` (Option, Optional): Output format. Choices: `text` (default), `json`.

#### Output Examples
**Text Format (Default)**:
```text
Location: Tokyo, Japan
Timezone: Asia/Tokyo (JST, UTC+09:00)
Local Time: 2026-07-02 18:30:15 (Thursday)
```

**JSON Format**:
```json
{
  "query": "Tokyo",
  "resolved_location": "Tokyo, Japan",
  "timezone": "Asia/Tokyo",
  "abbreviation": "JST",
  "utc_offset": "+09:00",
  "local_datetime": "2026-07-02T18:30:15+09:00",
  "epoch_timestamp": 1783017015
}
```

---

### 2. `convert`
Converts a specific datetime from a source location to one or more target locations.

#### CLI Command Schema
```bash
tz-cli convert --time <datetime> --from <source_location> --to <target_locations> [options]
```

#### Options
* `-t, --time <datetime>` (Option, Required): The datetime to convert. Expected format: `YYYY-MM-DD HH:MM`.
* `-f, --from <location>` (Option, Required): The source location/timezone of the input datetime.
* `-o, --to <locations>` (Option, Required, Multiple): The target location(s). Can be specified multiple times or as a comma-separated list (e.g., `-o "London" -o "New York"` or `-o "London,New York"`).
* `--json` (Flag, Optional): Outputs results in structured JSON instead of a text table.

#### Output Examples
**Text Table Format (Default)**:
```text
Converting: 2026-07-02 15:00 from Taipei, Taiwan (Asia/Taipei)

Location             Local Time            Date Offset  Timezone
----------------------------------------------------------------
Taipei, Taiwan       2026-07-02 15:00:00   [Source]     Asia/Taipei (+08:00)
London, UK           2026-07-02 08:00:00   Same Day     Europe/London (+01:00)
New York, USA        2026-07-02 03:00:00   Same Day     America/New_York (-04:00)
```

---

### 3. `schedule`
Finds and recommends the best overlapping meeting time intervals for participants distributed across multiple locations.

#### CLI Command Schema
```bash
tz-cli schedule --locations <locations> --date <date> --duration <duration> [options]
```

#### Options
* `-l, --locations <locations>` (Option, Required): Comma-separated list of participant locations (e.g., `"Taipei,London,New York"`).
* `-d, --date <date>` (Option, Required): Target meeting date. Format: `YYYY-MM-DD`.
* `-u, --duration <duration>` (Option, Optional): Meeting duration. Default: `1h`. Format: `<int>[h|m]` (e.g., `1h`, `30m`, `1.5h`).
* `-r, --range <hours>` (Option, Optional): Allowed "business/reasonable hours" local range. Default: `08:00-21:00`. Format: `HH:MM-HH:MM`.
* `-x, --export <filename>` (Option, Optional): Exports the top recommended meeting proposal to an `.ics` file.
* `--json` (Flag, Optional): Outputs recommended proposals in JSON format.

#### Output Examples
**Text Format (Default)**:
```text
Scheduling 1.0 hour meeting for Taipei, London, New York on 2026-07-03.
Business hours window: 08:00-21:00 local time.

Recommended Meeting Times (Ranked by overlap suitability):

[Rank 1] Score: 0.95 (Best overlap)
----------------------------------
Taipei (Local):    2026-07-03 16:00 - 17:00
London (Local):    2026-07-03 09:00 - 10:00
New York (Local):  2026-07-03 04:00 - 05:00 (Early morning)
UTC Time:          2026-07-03 08:00 - 09:00

[Rank 2] Score: 0.85
----------------------------------
Taipei (Local):    2026-07-03 17:00 - 18:00
London (Local):    2026-07-03 10:00 - 11:00
New York (Local):  2026-07-03 05:00 - 06:00
UTC Time:          2026-07-03 09:00 - 10:00

Google Calendar Quick Link (Rank 1):
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Cross+Timezone+Meeting&dates=20260703T080000Z/20260703T090000Z&details=Locations:+Taipei,+London,+New+York

To export the top proposal to an ICS file, run:
tz-cli schedule -l "Taipei,London,New York" -d "2026-07-03" -u "1h" -x "meeting.ics"
```

---

## Exit Codes

All CLI operations must exit with one of the following codes:

| Exit Code | Classification | Description |
|-----------|----------------|-------------|
| `0` | Success | Command executed successfully and finished operations. |
| `1` | Argument / Input Error | Missing required arguments, invalid datetime formats, or unsupported CLI option flags. |
| `2` | Resolution / API Error | Could not resolve location names, geocoding API timed out, or IANA timezone not found. |
