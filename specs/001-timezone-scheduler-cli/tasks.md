# Tasks: Timezone Scheduler CLI

**Input**: Design documents from `/specs/001-timezone-scheduler-cli/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Under our project constitution, writing automated tests (Unit & Integration tests) is **MANDATORY** for all new functionality.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure `src/` and `tests/` at repository root
- [X] T002 Initialize Python environment and register dependencies in `requirements.txt`
- [X] T003 [P] Configure linting and formatting tools (create `.flake8` or `pyproject.toml`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Initialize SQLite cache database connection and table schema in `src/cache.py`
- [X] T005 [P] Seed local embedded database containing top cities and US zip codes in `src/cache.py`
- [X] T006 [P] Create standard custom CLI exceptions and exit code mapping (0, 1, 2) in `src/main.py`
- [X] T007 Setup pytest testing configurations and mock API fixtures in `tests/conftest.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 查詢目前日期與時間 (Priority: P1) 🎯 MVP

**Goal**: Query current date and time by timezone identifier, city location name, or US zip code.

**Independent Test**: Run `python -m src.main query "Taipei"` and verify current time is displayed in text or JSON format.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (TDD)**

- [ ] T008 [P] [US1] Create unit and integration tests for location query in `tests/test_timezone.py`

### Implementation for User Story 1

- [ ] T009 [US1] Implement location resolution logic (Nominatim API client + SQLite query cache) in `src/cache.py`
- [ ] T010 [US1] Implement local timezone datetime calculation using `zoneinfo` in `src/timezone.py`
- [ ] T011 [US1] Implement CLI `query` subcommand parsing, parameters, and stdout/stderr output logic in `src/main.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - 跨時區時間轉換與對照 (Priority: P2)

**Goal**: Convert a given source datetime to multiple target locations and display a formatted offset table.

**Independent Test**: Run `python -m src.main convert --time "2026-07-02 15:00" --from "Taipei" --to "London" --to "New York"` and verify correct time conversion table.

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (TDD)**

- [ ] T012 [P] [US2] Create unit and integration tests for time conversion in `tests/test_timezone.py`

### Implementation for User Story 2

- [ ] T013 [US2] Implement timezone translation and daylight-saving time boundary checks in `src/timezone.py`
- [ ] T014 [US2] Implement stdout ASCII table layout and JSON structure conversion formatters in `src/main.py`
- [ ] T015 [US2] Implement CLI `convert` subcommand parsing and flag validation in `src/main.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 尋找共同合適的會議時間 (Priority: P2)

**Goal**: Automatically recommend ranked overlapping meeting times and export to RFC-compliant iCalendar (.ics) files.

**Independent Test**: Run `python -m src.main schedule --locations "Taipei,London,New York" --date "2026-07-03" --duration "1h" --export "meeting.ics"` and verify recommended slots and created file.

### Tests for User Story 3 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (TDD)**

- [ ] T016 [P] [US3] Create unit and integration tests for timezone scheduling overlap algorithm in `tests/test_scheduler.py`
- [ ] T017 [P] [US3] Create unit and integration tests for `.ics` file generator and calendar quick link in `tests/test_exporter.py`

### Implementation for User Story 3

- [ ] T018 [US3] Implement overlapping suitability calculation and ranking logic in `src/scheduler.py`
- [ ] T019 [US3] Implement RFC 5545 iCalendar serialization string writer and Google Calendar url builder in `src/exporter.py`
- [ ] T020 [US3] Implement CLI `schedule` subcommand parsing, custom `--range` boundaries, and `--export` export handling in `src/main.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T021 [P] Standardize CLI usage description, `--help` formatting, and CLI arguments documentation in `src/main.py`
- [ ] T022 [P] Complete and verify runnable scripts described in `quickstart.md`
- [ ] T023 Run manual integration validation scenarios to verify overall stability
- [ ] T024 Run code coverage checks and verify test coverage is >= 80% (`pytest --cov=src`)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 resolver
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1 and US2 components

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Data queries/models before services
- Service algorithms before CLI presentation
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 3

```bash
# Launch all tests for User Story 3 together:
Task: "Create unit and integration tests for timezone scheduling overlap algorithm in tests/test_scheduler.py"
Task: "Create unit and integration tests for .ics file generator and calendar quick link in tests/test_exporter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
