---

description: "Task list for LLM Dynamic Quiz and Feedback feature implementation"
---

# Tasks: LLM Dynamic Quiz and Feedback

**Input**: Design documents from `/specs/001-llm-quiz-feedback/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The tasks below include test tasks, as the plan implicitly covers testing.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (src/, tests/ and subdirectories per plan.md)
- [x] T002 Install dependencies (from requirements.txt, ensure Gemini API client is listed)
- [x] T003 [P] Document environment variable setup for GEMINI_API_KEY (in specs/001-llm-quiz-feedback/quickstart.md)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement SQLite database initialization and basic schema for Student, Question, QuizSession, PerformanceHistory entities in src/models/models.py and src/services/database.py.
- [x] T005 [P] Configure application-wide logging in src/services/logging_service.py.
- [x] T006 [P] Create base LLM client in src/services/llm_service.py for API key retrieval and basic connection.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dynamic Question Generation (P1) 🎯 MVP

**Goal**: Student receives new, relevant questions from LLM.

**Independent Test**: A student can start a quiz and see dynamically generated questions for the selected subject and difficulty band.

### Implementation for User Story 1

- [x] T007 [P] [US1] Implement LLM question generation function in src/services/llm_service.py based on specs/001-llm-quiz-feedback/contracts/llm_question_api.md.
- [x] T008 [P] [US1] Implement robust error handling and retry logic for LLM API calls in src/services/llm_service.py (FR-007).
- [x] T009 [US1] Modify UI to display dynamically generated questions (e.g., src/ui/english_exercise_view.py, src/ui/math_lesson_view.py).
- [x] T010 [P] [US1] Create unit test for LLM service's question generation in tests/unit/test_llm_service.py.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 3 - Instant Explanatory Feedback (P1)

**Goal**: Student receives immediate explanation after answering.

**Independent Test**: After submitting an answer, the student sees a clear explanation for the correct answer.

### Implementation for User Story 3

- [x] T011 [P] [US3] Ensure LLM response processing includes extracting explanations in src/services/llm_service.py.
- [x] T012 [US3] Modify UI to display question explanations after submission (e.g., src/ui/english_exercise_view.py, src/ui/math_lesson_view.py).
- [x] T013 [P] [US3] Create unit test for feedback display logic in the UI (e.g., tests/unit/test_ui.py).

**Checkpoint**: At this point, User Stories 1 AND 3 should both work independently

---

## Phase 5: User Story 2 - Personalized Question Adaptation (P2)

**Goal**: System adapts questions based on student performance history.

**Independent Test**: System adapts question selection based on recorded student performance, e.g., more difficult questions after correct streaks.

### Implementation for User Story 2

- [x] T014 [P] [US2] Implement Student entity CRUD operations in src/services/data_service.py based on specs/001-llm-quiz-feedback/contracts/local_data_interface.md.
- [x] T015 [P] [US2] Implement QuizSession entity CRUD operations in src/services/data_service.py based on specs/001-llm-quiz-feedback/contracts/local_data_interface.md.
- [x] T016 [P] [US2] Implement PerformanceHistory entity CRUD operations and deletion in src/services/data_service.py based on specs/001-llm-quiz-feedback/contracts/local_data_interface.md.
- [x] T017 [US2] Implement adaptive_learning_service.py to analyze PerformanceHistory and determine next difficulty_band/context_history for LLM prompt. (This task will incorporate FR-011 and its explicit mappings).
- [x] T018 [US2] Integrate adaptive_learning_service.py output with LLM prompt generation in src/services/llm_service.py to adapt questions.
- [x] T019 [P] [US2] Create unit tests for data_service.py in tests/unit/test_data_service.py.
- [x] T020 [P] [US2] Create unit tests for adaptive_learning_service.py in tests/unit/test_adaptive_learning_service.py.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T021 Review and refine all error messages and user notifications for a better UX.
- [x] T022 Conduct basic performance testing for LLM interaction and local data operations.
- [x] T023 Update specs/001-llm-quiz-feedback/quickstart.md with detailed instructions for running and testing the feature.
- [x] T024 Create integration tests for the overall quiz flow, covering dynamic generation, feedback, and adaptation in tests/integration/test_app_flow.py.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2...)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (Dynamic Question Generation - P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (Instant Explanatory Feedback - P1)**: Can start after Foundational (Phase 2) - Integrates with US1 components (LLM response processing)
- **User Story 2 (Personalized Question Adaptation - P2)**: Can start after Foundational (Phase 2) - Integrates with US1 and US3 components (LLM prompt generation, data storage)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Story 1, User Story 3, and User Story 2 can be worked on in parallel by different team members, though US3 and US2 will build upon US1's core functionality.
- All tests for a user story marked [P] can run in parallel
- Specific implementation tasks marked [P] within a story can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "T010 [P] [US1] Create unit test for LLM service's question generation in tests/unit/test_llm_service.py"

# Launch parallel implementation tasks for User Story 1:
Task: "T007 [P] [US1] Implement LLM question generation function in src/services/llm_service.py based on specs/001-llm-quiz-feedback/contracts/llm_question_api.md"
Task: "T008 [P] [US1] Implement robust error handling and retry logic for LLM API calls in src/services/llm_service.py (FR-007)"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 3
5. **STOP and VALIDATE**: Test User Stories 1 and 3 independently and their combined functionality.
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test independently → Deploy/Demo
4. Add User Story 2 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 3 (can start after T007)
   - Developer C: User Story 2 (can start after foundational data services are available)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence