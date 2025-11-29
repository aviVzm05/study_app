# Tasks: Kids Learning App

**Input**: Design documents from `specs/001-kids-learning-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - for this project, unit and integration tests will be generated as part of the 'Polish & Cross-Cutting Concerns' phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directories: `src/models/`, `src/services/`, `src/ui/`, `tests/integration/`, `tests/unit/`, `database/`
- [X] T002 Initialize Python project with a virtual environment in the project root.
- [X] T003 [P] Create `requirements.txt` with `PyQt6` and `pytest` in the project root.
- [X] T004 Install core dependencies from `requirements.txt`.
- [X] T005 [P] Configure `pytest` (e.g., `pytest.ini` if needed).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create `src/main.py` for the application entry point.
- [X] T007 Implement base SQLite database connection and utility functions in `src/services/database.py`.
- [X] T008 Implement database schema creation from `data-model.md` in `src/models/schema.py`.
- [X] T009 Implement base data models for `subjects`, `topics`, `lessons`, `questions`, and `progress` tables (e.g., ORM models or direct SQL wrappers) in `src/models/`.
- [X] T010 Implement database seeding logic for initial content (1 topic per subject per grade for MVP) in `src/services/data_seeder.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Math Skill Building (Priority: P1) 🎯 MVP

**Goal**: As a student, I want to select a math topic relevant to my grade, receive a simple explanation of the core concept, and then solve practice problems to ensure I have understood it.

**Independent Test**: A user can select a grade and a math topic, view the lesson, and complete a set of 5 practice problems, receiving feedback on their answers.

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement UI for grade selection in `src/ui/grade_selection_view.py`.
- [X] T012 [P] [US1] Implement UI for subject/topic selection in `src/ui/topic_selection_view.py`.
- [X] T013 [US1] Implement service for fetching math lessons and questions in `src/services/math_service.py`.
- [X] T014 [US1] Implement UI for displaying math lessons and practice problems in `src/ui/math_lesson_view.py`.
- [X] T015 [US1] Implement logic for validating math answers and providing feedback in `src/services/math_validation.py`.
- [X] T016 [US1] Integrate math learning flow into `src/main.py` and connect UI views.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - English Writing Practice (Priority: P2)

**Goal**: As a student, I want to practice my English writing by constructing sentences based on a prompt, have my submission validated for basic grammar and spelling, and receive guidance on my mistakes.

**Independent Test**: A user can select an English writing exercise, receive a prompt, write a sentence, and get immediate feedback on its correctness.

### Implementation for User Story 2

- [X] T017 [P] [US2] Implement service for fetching English lessons and writing prompts in `src/services/english_service.py`.
- [X] T018 [US2] Implement UI for English writing exercises in `src/ui/english_exercise_view.py`.
- [X] T019 [US2] Implement offline validation for English grammar and spelling (basic rules) in `src/services/english_validation.py`.
- [X] T020 [US2] Integrate English learning flow into `src/main.py` and connect UI views.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Offline Accessibility (Priority: P3)

**Goal**: As a student, I want to access all my math and English lessons and practice exercises without an internet connection, so I can continue learning from anywhere at any time.

**Independent Test**: With the device in airplane mode, a user can launch the app, navigate to a lesson, and complete a practice quiz.

### Implementation for User Story 3

- [X] T021 [US3] Verify all content loading mechanisms use only the local SQLite database.
- [X] T022 [US3] Implement local progress saving and loading functionality in `src/services/progress_service.py`.
- [X] T023 [US3] Ensure UI handles (and does not attempt) any online features gracefully in `src/main.py` and relevant UI views.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T024 [P] Implement basic error handling across the application.
- [ ] T025 [P] Add logging for key application events (e.g., lesson started, quiz completed) in `src/services/logging_service.py`.
- [ ] T026 [P] Write unit tests for `src/services/math_service.py`.
- [ ] T027 [P] Write unit tests for `src/services/english_service.py`.
- [ ] T028 [P] Write unit tests for `src/services/database.py`.
- [ ] T029 [P] Write integration tests for core user flows (e.g., complete math lesson) in `tests/integration/`.
- [ ] T030 Create `README.md` for the project with setup, run, and test instructions.
- [ ] T031 Final code review and refactoring for maintainability.
- [ ] T032 Build and package the application for target platforms (Windows, macOS, Linux).

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Many implementation tasks within a user story can be parallelized (marked [P]).

---

## Parallel Example: User Story 1

```bash
# Launch UI components for User Story 1 together:
Task: "Implement UI for grade selection in src/ui/grade_selection_view.py"
Task: "Implement UI for subject/topic selection in src/ui/topic_selection_view.py"
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

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (where applicable, for future TDD adoption)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
