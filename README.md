# 🎮 Agentic Game Debugger

**Agentic AI Pipeline for Automated Bug Detection, Root Cause Analysis, and Fixing in Video Games Using LangGraph**

An academic proof-of-concept demonstrating how specialised AI agents, orchestrated through a LangGraph state graph, can automatically detect bugs in video-game code, diagnose their root causes, generate targeted patches, run regression tests, and route failed fixes through a controlled retry loop or human-review escalation.

> **Note:** This is an educational demonstration, not a production debugging platform. It uses deterministic (rule-based) agents and predefined game bugs. No API key is required to run the demo.

---

## ✨ Features

- **5 specialised agents** — Bug Detector, Root Cause Analyser, Fix Generator, Test Verifier, Decision Agent
- **LangGraph orchestration** — `StateGraph` with typed state, normal edges, conditional edges, and a retry loop
- **3 demo bug scenarios** — health boundary, inventory capacity, enemy AI state management
- **Automated testing** — pytest runs before and after the patch in an isolated temp directory
- **Conditional routing** — success / retry / human-review based on test results
- **Safe execution** — patches are applied only to temporary copies; originals are never modified
- **Interactive Streamlit UI** — professional dashboard with tabbed results, diff viewer, and downloadable reports
- **No API key required** — fully deterministic mode works out of the box

---

## 🏗️ Architecture

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

| Edge Type | Description |
|---|---|
| **Normal** | Sequential flow between agents |
| **Conditional** | Decision agent routes to success, retry, or human review |
| **Retry loop** | Failed fixes loop back to fix_generator (max 2 retries) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Workflow Engine | LangGraph ≥ 0.2.0 |
| Web Interface | Streamlit ≥ 1.36.0 |
| Testing | pytest ≥ 7.0.0 |
| State Validation | Pydantic ≥ 2.0.0 |
| Documents | python-pptx, python-docx |

---

## 📁 Repository Structure

```text
agentic-game-debugger/
├── app/                        # Streamlit web interface
│   ├── main.py                 # Entry point
│   └── components/
│       ├── dashboard.py        # Metrics, bug selection, source viewer
│       └── results.py          # Tabbed pipeline results
├── agents/                     # Specialised LangGraph agents
│   ├── bug_detector.py         # Pattern-based bug detection
│   ├── root_cause_analyzer.py  # Root cause diagnosis
│   ├── fix_generator.py        # Patch generation
│   ├── test_verifier.py        # Isolated test execution
│   └── decision_agent.py       # Routing decisions
├── graph/                      # LangGraph orchestration
│   ├── state.py                # PipelineState TypedDict
│   ├── workflow.py             # Graph builder & runner
│   └── routing.py              # Conditional edge logic
├── game_project/               # Sample game with intentional bugs
│   ├── player.py               # Health bug (BUG-001)
│   ├── inventory.py            # Capacity bug (BUG-002)
│   └── enemy_ai.py             # State-reset bug (BUG-003)
├── bug_cases/                  # Structured bug reports (JSON)
│   ├── health_bug.json
│   ├── inventory_bug.json
│   └── enemy_ai_bug.json
├── tests/                      # Automated tests
│   ├── test_health.py          # Player health tests
│   ├── test_inventory.py       # Inventory capacity tests
│   ├── test_enemy_ai.py        # Enemy AI state tests
│   └── test_workflow.py        # Full pipeline integration tests
├── scripts/
│   └── run_demo.py             # CLI pipeline runner
├── docs/
│   ├── Architecture.md         # Detailed architecture docs
│   └── Project_Report.docx     # Project report
├── presentation/
│   └── Project_Presentation.pptx
├── sample_outputs/             # Example pipeline outputs
├── .env.example                # Optional LLM configuration
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or newer
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/agentic-game-debugger.git
cd agentic-game-debugger

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Streamlit Web Interface (recommended)

```bash
streamlit run app/main.py
```

Open the URL printed by Streamlit (usually `http://localhost:8501`).

### CLI Demo

```bash
python scripts/run_demo.py health      # Health boundary bug
python scripts/run_demo.py inventory   # Inventory capacity bug
python scripts/run_demo.py enemy_ai    # Enemy AI state bug
```

---

## 🧪 Running Tests

### Confirm bugs exist (these tests FAIL intentionally)

```bash
pytest tests/test_health.py tests/test_inventory.py tests/test_enemy_ai.py -v
```

Expected: **4 failures** (2 health, 1 inventory, 1 enemy AI) + 12 passes.

### Full pipeline integration tests

```bash
pytest tests/test_workflow.py -v
```

Expected: **6 passed** — verifies all bugs are detected, fixed, and verified.

### All tests

```bash
pytest tests/ -v
```

---

## 🐛 Demo Bug Scenarios

### Bug 1: Player Health Can Become Negative
- **File:** `game_project/player.py` → `Player.take_damage`
- **Issue:** `self.health -= amount` with no lower-bound check
- **Fix:** `self.health = max(0, self.health - amount)`

### Bug 2: Inventory Exceeds Maximum Capacity
- **File:** `game_project/inventory.py` → `Inventory.add_item`
- **Issue:** Items appended without checking `self.capacity`
- **Fix:** Guard with `if len(self.items) >= self.capacity: return False`

### Bug 3: Enemy AI State Does Not Reset
- **File:** `game_project/enemy_ai.py` → `EnemyAI.update`
- **Issue:** Missing `else` branch to reset state to `IDLE`
- **Fix:** Add `else: self.state = self.IDLE`

---

## 🔧 Optional LLM Configuration

The demo runs in fully deterministic mode with no API key. To optionally enable LLM-enhanced diagnosis:

```bash
cp .env.example .env
# Edit .env and set your provider/key
```

---

## ⚠️ Limitations & Safety

- This is an **educational proof of concept**, not a production debugging system.
- All agents use **deterministic, rule-based logic** — no LLM is required or invoked in the default mode.
- Patches are applied only to **temporary copies** in isolated directories.
- Original source files are **never modified** by the pipeline.
- The system does **not** execute arbitrary code, connect to external services, or modify system files.
- Test execution has a **30-second timeout** to prevent runaway processes.

---

## 🔮 Future Enhancements

- LLM-powered bug detection and patch generation with schema validation
- Support for PDF/image bug reports with OCR
- Multi-file patch support
- Duplicate bug detection
- Persistent audit logs and review decisions
- Authentication and role-based access
- Integration with game engines (Unity, Unreal) via plugins
- Configurable risk policies and approval workflows

---

## 📄 Documentation

- **Architecture:** `docs/Architecture.md`
- **Project Report:** `docs/Project_Report.docx`
- **Presentation:** `presentation/Project_Presentation.pptx`

---

## 📜 License

This project is for educational and academic purposes.

---

Built with Python · LangGraph · Streamlit · pytest
