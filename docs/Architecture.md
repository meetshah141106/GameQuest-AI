# System Architecture

## Pipeline Overview

The Agentic Game Debugger uses a **LangGraph `StateGraph`** to orchestrate five specialised agents that collaboratively detect, diagnose, fix, and verify bugs in video-game code.

## Graph Structure

```text
START
  │
  ▼
bug_detector ──► root_cause_analyzer ──► fix_generator ◄─── retry_fix
                                              │                  ▲
                                              ▼                  │
                                        test_verifier            │
                                              │                  │
                                              ▼                  │
                                       decision_agent ───────────┘
                                        ╱          ╲
                                   fix_success   human_review
                                     │               │
                                    END             END
```

### Edge Types

| Edge | Type | Description |
|---|---|---|
| START → bug_detector | Normal | Entry point |
| bug_detector → root_cause_analyzer | Normal | Sequential |
| root_cause_analyzer → fix_generator | Normal | Sequential |
| fix_generator → test_verifier | Normal | Sequential |
| test_verifier → decision_agent | Normal | Sequential |
| decision_agent → fix_success | **Conditional** | Tests passed |
| decision_agent → retry_fix (→ fix_generator) | **Conditional** | Tests failed, retries remain |
| decision_agent → human_review | **Conditional** | Retries exhausted or safety issue |
| fix_success → END | Normal | Terminal |
| human_review → END | Normal | Terminal |

### Retry Loop

The conditional edge from `decision_agent` back to `fix_generator` creates a controlled retry loop.  The loop terminates when:
- Tests pass (→ `fix_success`).
- The attempt count reaches `max_attempts` (→ `human_review`).
- A safety condition is violated (→ `human_review`).

## State Schema

The `PipelineState` TypedDict carries all data between nodes:

| Group | Fields |
|---|---|
| **Input** | `bug_report`, `source_code`, `source_file`, `test_file` |
| **Detection** | `bug_type`, `severity`, `affected_function`, `evidence`, `detection_confidence`, `detection_summary` |
| **Root Cause** | `root_cause`, `faulty_condition`, `recommendation` |
| **Fix** | `original_code`, `fixed_code`, `patch_explanation`, `patch_diff` |
| **Testing** | `baseline_test_output`, `baseline_tests_passed`, `post_fix_test_output`, `post_fix_tests_passed` |
| **Decision** | `attempt_count`, `max_attempts`, `decision`, `route`, `review_reasons`, `previous_failures` |
| **Final** | `status`, `final_outcome`, `workflow_history` |

## Agent Responsibilities

1. **Bug Detector** — pattern-matches source code against known bug signatures (boundary-condition, state-management). Produces classification, severity, evidence, and confidence score.

2. **Root Cause Analyser** — explains *why* the code fails, identifies the faulty condition, and recommends a minimal fix.

3. **Fix Generator** — produces a targeted string-replacement patch and a unified diff. Never modifies the original source file.

4. **Test Verifier** — copies the project to an isolated temp directory, runs `pytest` before (baseline) and after (post-fix) applying the patch, and returns structured results.

5. **Decision Agent** — deterministic rules: accept if tests pass, retry if attempts remain, escalate to human review otherwise.

## Safety Measures

- Patches are applied only to **temporary copies** of the source files.
- Original project files are **never modified**.
- Tests run in a **subprocess** with a 30-second timeout.
- No arbitrary shell commands are executed.
- Path traversal in patch targets is not possible (patches target known files only).
- The demo runs **without any API key** in fully deterministic mode.
