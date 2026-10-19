"""Generate the PowerPoint presentation and Word report.

Usage::

    python scripts/generate_docs.py
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

# ═══════════════════════════════════════════════════════════════
#  PowerPoint Generation
# ═══════════════════════════════════════════════════════════════

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


def _set_slide_bg(slide, r, g, b):
    """Set a solid background colour for a slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(r, g, b)


def _add_text_box(slide, left, top, width, height, text,
                  font_size=18, bold=False, color=(255, 255, 255),
                  alignment=PP_ALIGN.LEFT):
    """Helper to add a styled text box."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = RGBColor(*color)
    p.alignment = alignment
    return tf


def _add_bullet_frame(slide, left, top, width, height, items,
                      font_size=16, color=(220, 220, 220)):
    """Add a text box with bullet points."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = RGBColor(*color)
        p.space_after = Pt(6)
    return tf


def generate_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    BG = (30, 27, 46)
    ACCENT = (124, 58, 237)
    PINK = (236, 72, 153)
    WHITE = (255, 255, 255)
    GRAY = (180, 180, 190)

    # ── Slide 1: Title ──────────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 1.5, 1.5, 10, 1, "🎮", font_size=60, alignment=PP_ALIGN.CENTER)
    _add_text_box(slide, 1, 2.5, 11, 1.5,
                  "Agentic AI Pipeline for Automated Bug Detection\nand Fixing in Video Games",
                  font_size=32, bold=True, alignment=PP_ALIGN.CENTER)
    _add_text_box(slide, 1, 4.2, 11, 0.8,
                  "Using LangGraph • Python • Streamlit",
                  font_size=20, color=GRAY, alignment=PP_ALIGN.CENTER)
    _add_text_box(slide, 1, 5.5, 11, 0.5,
                  "Academic Proof of Concept",
                  font_size=16, color=GRAY, alignment=PP_ALIGN.CENTER)

    # ── Slide 2: Background & Motivation ─────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Background & Motivation",
                  font_size=30, bold=True, color=PINK)
    _add_bullet_frame(slide, 0.8, 1.5, 11.5, 5.5, [
        "Video-game codebases involve complex interactions: physics, AI, inventory, quests, rendering",
        "Bugs cause crashes, incorrect gameplay, and poor player experiences",
        "Traditional debugging is manual: reproduce → inspect → trace → fix → retest",
        "AI-assisted debugging can automate repetitive diagnostic steps",
        "Agentic AI divides the workflow into specialised, coordinated agents",
        "LangGraph provides structured orchestration with state management and conditional routing",
        "Goal: demonstrate a working multi-agent debugging pipeline for game code",
    ])

    # ── Slide 3: Problem Statement ───────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Problem Statement",
                  font_size=30, bold=True, color=PINK)
    _add_bullet_frame(slide, 0.8, 1.5, 11.5, 5.5, [
        "Game developers spend significant time on manual bug diagnosis",
        "Boundary-condition errors, state-management bugs, and logic errors are common",
        "These bugs often require deep knowledge of multiple interacting systems",
        "No standardised pipeline exists for automated game-bug diagnosis and patching",
        "Need: a structured, safe, and transparent agentic workflow that can detect bugs,",
        "  analyse root causes, generate targeted fixes, test them, and route failures",
    ])

    # ── Slide 4: Objectives ──────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Project Objectives",
                  font_size=30, bold=True, color=PINK)
    _add_bullet_frame(slide, 0.8, 1.5, 11.5, 5.5, [
        "Accept bug reports, error logs, and source code as input",
        "Detect bugs using deterministic pattern analysis",
        "Analyse root causes grounded in the actual source code",
        "Generate minimal, targeted code patches",
        "Apply fixes safely to temporary copies only",
        "Run automated tests before and after the patch",
        "Route results: accept fix, retry, or escalate to human review",
        "Present the workflow through an interactive Streamlit interface",
        "Run without any API key in fully deterministic demo mode",
    ])

    # ── Slide 5: Existing Limitations ────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Limitations of Traditional Debugging",
                  font_size=30, bold=True, color=PINK)
    _add_bullet_frame(slide, 0.8, 1.5, 5.5, 5.5, [
        "Manual reproduction of issues",
        "Time-consuming log inspection",
        "Requires deep system knowledge",
        "No automated root-cause analysis",
        "Fixes applied without isolation",
        "No structured retry mechanism",
    ], font_size=15)
    _add_text_box(slide, 7, 1.3, 5, 0.6, "Our Approach →",
                  font_size=18, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 7, 2.0, 5.5, 5, [
        "Automated pattern-based detection",
        "Structured root-cause explanations",
        "Targeted patch generation",
        "Isolated testing in temp directories",
        "Conditional routing & retry loops",
        "Human-in-the-loop escalation",
    ], font_size=15)

    # ── Slide 6: Proposed Solution ───────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Proposed Agentic AI Solution",
                  font_size=30, bold=True, color=PINK)
    _add_text_box(slide, 0.8, 1.5, 11.5, 1.5,
                  "A LangGraph-based pipeline of 5 specialised agents that collaboratively\n"
                  "detect, diagnose, fix, and verify bugs in video-game code.\n\n"
                  "Key Design Principles:",
                  font_size=17, color=GRAY)
    _add_bullet_frame(slide, 0.8, 3.5, 11.5, 3.5, [
        "Each agent has a single, well-defined responsibility",
        "Shared TypedDict state enables transparent data flow",
        "Conditional edges allow branching based on test results",
        "Retry loop with configurable maximum attempts",
        "Human-review escalation for unresolved or risky cases",
        "Safe patch application: originals never modified",
    ])

    # ── Slide 7: Architecture Diagram ────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.3, 11, 0.8, "System Architecture",
                  font_size=30, bold=True, color=PINK)
    arch_text = (
        "START\n"
        "  │\n"
        "  ▼\n"
        "Bug Detector  ──►  Root Cause Analyser  ──►  Fix Generator  ◄── retry\n"
        "                                                   │                 ▲\n"
        "                                                   ▼                 │\n"
        "                                             Test Verifier           │\n"
        "                                                   │                 │\n"
        "                                                   ▼                 │\n"
        "                                            Decision Agent ──────────┘\n"
        "                                             ╱          ╲\n"
        "                                        Success      Human Review\n"
        "                                          │               │\n"
        "                                         END             END"
    )
    _add_text_box(slide, 1.0, 1.3, 11, 5.5, arch_text,
                  font_size=14, color=(200, 200, 255))

    # ── Slide 8: LangGraph Details ───────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "LangGraph Implementation Details",
                  font_size=30, bold=True, color=PINK)
    _add_bullet_frame(slide, 0.8, 1.5, 5.5, 5.5, [
        "StateGraph with PipelineState TypedDict",
        "7 nodes: 5 agents + 2 terminal nodes",
        "5 normal edges for sequential flow",
        "1 conditional edge with 3 branches:",
        "  → fix_success (tests passed)",
        "  → retry_fix (tests failed, retries left)",
        "  → human_review (exhausted or unsafe)",
        "State preserves full workflow history",
    ], font_size=15)
    _add_text_box(slide, 7, 1.3, 5.5, 0.6, "State Groups:",
                  font_size=18, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 7, 2.0, 5.5, 5, [
        "Input: bug_report, source_code, test_file",
        "Detection: bug_type, severity, confidence",
        "Root Cause: explanation, faulty condition",
        "Fix: original_code, fixed_code, diff",
        "Testing: baseline & post-fix results",
        "Decision: route, attempts, review reasons",
        "Final: status, outcome, history",
    ], font_size=14)

    # ── Slide 9: Sample Bugs ─────────────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Demo Bug Scenarios",
                  font_size=30, bold=True, color=PINK)
    bugs = [
        ("BUG-001: Health Goes Negative", "player.py → take_damage",
         "self.health -= amount", "self.health = max(0, self.health - amount)"),
        ("BUG-002: Inventory Exceeds Capacity", "inventory.py → add_item",
         "self.items.append(item)  # no check", "if len >= capacity: return False"),
        ("BUG-003: Enemy AI Stuck in Pursuit", "enemy_ai.py → update",
         "Missing else clause", "else: self.state = self.IDLE"),
    ]
    for i, (title, loc, buggy, fix) in enumerate(bugs):
        y = 1.5 + i * 1.9
        _add_text_box(slide, 0.8, y, 11, 0.4, title,
                      font_size=18, bold=True, color=ACCENT)
        _add_text_box(slide, 0.8, y + 0.45, 11, 0.35,
                      f"File: {loc}",
                      font_size=14, color=GRAY)
        _add_text_box(slide, 0.8, y + 0.85, 5, 0.35,
                      f"Buggy: {buggy}", font_size=13, color=(255, 130, 130))
        _add_text_box(slide, 6.5, y + 0.85, 6, 0.35,
                      f"Fix: {fix}", font_size=13, color=(130, 255, 130))

    # ── Slide 10: Patch & Verification ───────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Patch Generation & Verification",
                  font_size=30, bold=True, color=PINK)
    _add_bullet_frame(slide, 0.8, 1.5, 5.5, 2.5, [
        "Fix Generator produces a string-replacement patch",
        "Unified diff generated for review",
        "Patch applied to temporary copy only",
        "Original source files never modified",
    ], font_size=15)
    _add_text_box(slide, 0.8, 4.0, 5, 0.5, "Verification Process:",
                  font_size=18, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 0.8, 4.6, 5.5, 2.5, [
        "1. Copy project to isolated temp directory",
        "2. Run tests on buggy code (baseline — should fail)",
        "3. Apply patch to temp copy",
        "4. Run tests again (post-fix — should pass)",
        "5. Return structured pass/fail results",
    ], font_size=14)
    _add_text_box(slide, 7, 1.5, 5.5, 0.5, "Safety Measures:",
                  font_size=18, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 7, 2.1, 5.5, 4.5, [
        "Isolated temp directory per attempt",
        "30-second test timeout",
        "No arbitrary shell commands",
        "Path traversal not possible",
        "Subprocess execution with captured output",
        "Controlled pytest runner only",
    ], font_size=14)

    # ── Slide 11: Results & Limitations ──────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Results, Limitations & Safety",
                  font_size=30, bold=True, color=PINK)
    _add_text_box(slide, 0.8, 1.3, 5, 0.5, "Results:",
                  font_size=20, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 0.8, 1.9, 5.5, 2.5, [
        "All 3 bugs detected with 92–95% confidence",
        "All 3 patches verified by automated tests",
        "Pipeline correctly routes to success",
        "Retry and human-review paths functional",
        "22 tests (16 game + 6 pipeline) validate the system",
    ], font_size=14)
    _add_text_box(slide, 0.8, 4.2, 5, 0.5, "Limitations:",
                  font_size=20, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 0.8, 4.8, 5.5, 2.5, [
        "Deterministic only — no real LLM integration yet",
        "Handles predefined bug patterns; not generalised",
        "Single-file patches; no multi-file support",
        "No real game engine integration",
        "Not a production security sandbox",
    ], font_size=14)
    _add_text_box(slide, 7, 1.3, 5.5, 0.5, "Key Numbers:",
                  font_size=20, bold=True, color=ACCENT)
    stats = [
        ("Agents", "5"), ("Bug Scenarios", "3"), ("Test Cases", "22"),
        ("Max Retries", "2"), ("Graph Nodes", "7"), ("Conditional Edges", "1"),
    ]
    for i, (label, val) in enumerate(stats):
        y = 2.0 + i * 0.5
        _add_text_box(slide, 7, y, 3, 0.4, label, font_size=15, color=GRAY)
        _add_text_box(slide, 10, y, 2, 0.4, val, font_size=15, bold=True)

    # ── Slide 12: Future & Conclusion ────────────────────
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _set_slide_bg(slide, *BG)
    _add_text_box(slide, 0.8, 0.5, 11, 0.8, "Future Enhancements & Conclusion",
                  font_size=30, bold=True, color=PINK)
    _add_text_box(slide, 0.8, 1.3, 5, 0.5, "Future Work:",
                  font_size=20, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 0.8, 1.9, 5.5, 3, [
        "LLM-powered detection and patch generation",
        "Multi-file and multi-language support",
        "Game-engine integration (Unity, Unreal)",
        "Persistent audit logs and review workflows",
        "Configurable risk policies",
        "Visual diff viewer with syntax highlighting",
    ], font_size=14)
    _add_text_box(slide, 0.8, 5.0, 11, 1.5,
                  "Conclusion: This PoC demonstrates that agentic AI, orchestrated through\n"
                  "LangGraph, can effectively structure the game-debugging workflow into\n"
                  "specialised, coordinated agents with safe execution and transparent results.",
                  font_size=17, color=GRAY)
    _add_text_box(slide, 7, 1.3, 5.5, 0.5, "Tech Stack:",
                  font_size=20, bold=True, color=ACCENT)
    _add_bullet_frame(slide, 7, 1.9, 5.5, 3, [
        "Python 3.10+",
        "LangGraph (StateGraph, conditional edges)",
        "Streamlit (interactive UI)",
        "pytest (automated testing)",
        "Pydantic (state validation)",
        "python-pptx / python-docx (documents)",
    ], font_size=14)

    out = _ROOT / "presentation" / "Project_Presentation.pptx"
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"✅ Saved: {out}")


# ═══════════════════════════════════════════════════════════════
#  Word Report Generation
# ═══════════════════════════════════════════════════════════════

from docx import Document
from docx.shared import Pt as DocPt, Inches as DocInches, RGBColor as DocRGB
from docx.enum.text import WD_ALIGN_PARAGRAPH


def _add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    return h


def _add_para(doc, text, bold=False, font_size=11):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = DocPt(font_size)
    run.bold = bold
    return p


def _add_table_row(table, cells_text):
    row = table.add_row()
    for i, text in enumerate(cells_text):
        row.cells[i].text = text


def generate_docx():
    doc = Document()

    # ── Title Page ───────────────────────────────────────
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("Agentic AI Pipeline for Automated Bug Detection\nand Fixing in Video Games Using LangGraph")
    run.font.size = DocPt(22)
    run.bold = True

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("Project Report\n\nAcademic Proof of Concept")
    run.font.size = DocPt(14)

    doc.add_page_break()

    # ── Abstract ─────────────────────────────────────────
    _add_heading(doc, "Abstract")
    _add_para(doc,
        "This report presents an Agentic AI pipeline for automated bug detection, "
        "root cause analysis, and fixing in video-game code. The system uses LangGraph "
        "to orchestrate five specialised agents — Bug Detector, Root Cause Analyser, "
        "Fix Generator, Test Verifier, and Decision Agent — through a structured "
        "state graph with normal edges, conditional routing, and a controlled retry "
        "loop. The proof of concept demonstrates the pipeline on three intentionally "
        "buggy game modules (player health, inventory capacity, and enemy AI state "
        "management), achieving successful automated detection, patching, and "
        "verification for all three scenarios without requiring any API key."
    )

    # ── Introduction ─────────────────────────────────────
    _add_heading(doc, "1. Introduction")
    _add_para(doc,
        "Video-game development involves complex interactions between game logic, "
        "physics engines, collision detection, player controls, inventory systems, "
        "enemy behaviour, quests, and rendering pipelines. Bugs in these systems "
        "can cause crashes, incorrect gameplay, unexpected behaviour, and poor "
        "player experiences. Traditional debugging workflows require developers to "
        "manually reproduce issues, inspect logs, trace execution paths, locate the "
        "underlying cause, implement a correction, and run regression tests.\n\n"
        "This project proposes an Agentic AI pipeline that divides the debugging "
        "process into specialised agents coordinated through LangGraph. Each agent "
        "performs a distinct task, passes structured results to subsequent agents, "
        "and participates in a controlled workflow that can retry failed fixes or "
        "request human intervention."
    )

    # ── Problem Statement ────────────────────────────────
    _add_heading(doc, "2. Problem Statement")
    _add_para(doc,
        "Game developers spend significant time on manual bug diagnosis. Boundary-"
        "condition errors, state-management bugs, and logic errors are common and "
        "often require deep knowledge of multiple interacting systems. No standardised "
        "pipeline exists for automated game-bug diagnosis and patching. There is a "
        "need for a structured, safe, and transparent agentic workflow that can detect "
        "bugs, analyse root causes, generate targeted fixes, test them, and route "
        "failures appropriately."
    )

    # ── Objectives ───────────────────────────────────────
    _add_heading(doc, "3. Objectives")
    objectives = [
        "Accept game-related bug reports, error logs, and relevant source code.",
        "Identify likely bugs using deterministic analysis.",
        "Analyse the probable root cause of detected bugs.",
        "Generate a targeted code patch.",
        "Apply fixes safely to a temporary copy of the sample project.",
        "Execute automated tests against the proposed fix.",
        "Detect whether the fix passes or fails.",
        "Retry or revise a failed fix within a configured limit.",
        "Escalate unresolved or risky cases to human review.",
        "Present the entire process through a web interface.",
        "Run without any API key in deterministic demo mode.",
    ]
    for obj in objectives:
        doc.add_paragraph(obj, style="List Bullet")

    # ── Technology Stack ─────────────────────────────────
    _add_heading(doc, "4. Technology Stack")
    table = doc.add_table(rows=1, cols=3)
    table.style = "Light Grid Accent 1"
    table.rows[0].cells[0].text = "Layer"
    table.rows[0].cells[1].text = "Technology"
    table.rows[0].cells[2].text = "Version"
    for row in [
        ("Language", "Python", "3.10+"),
        ("Workflow Engine", "LangGraph", "≥ 0.2.0"),
        ("Web Interface", "Streamlit", "≥ 1.36.0"),
        ("Testing", "pytest", "≥ 7.0.0"),
        ("State Validation", "Pydantic", "≥ 2.0.0"),
        ("Documents", "python-pptx, python-docx", "latest"),
    ]:
        _add_table_row(table, row)

    # ── Architecture ─────────────────────────────────────
    _add_heading(doc, "5. System Architecture")
    _add_para(doc,
        "The system uses a LangGraph StateGraph with 7 nodes (5 agents + 2 terminal "
        "nodes), 5 normal edges for sequential processing, and 1 conditional edge "
        "with 3 branches for decision routing."
    )

    _add_heading(doc, "5.1 Graph Structure", level=2)
    _add_para(doc,
        "START → bug_detector → root_cause_analyzer → fix_generator → test_verifier "
        "→ decision_agent → {fix_success | retry_fix | human_review} → END\n\n"
        "The retry_fix branch loops back to fix_generator, creating a controlled "
        "retry mechanism with a configurable maximum attempt count (default: 3).",
        font_size=10
    )

    _add_heading(doc, "5.2 State Schema", level=2)
    _add_para(doc,
        "The PipelineState TypedDict carries all data between nodes, organised into "
        "groups: Input (bug_report, source_code, test_file), Detection (bug_type, "
        "severity, confidence), Root Cause (explanation, faulty_condition), Fix "
        "(original_code, fixed_code, diff), Testing (baseline and post-fix results), "
        "Decision (route, attempts, review_reasons), and Final (status, outcome, "
        "workflow_history)."
    )

    # ── Agent Responsibilities ───────────────────────────
    _add_heading(doc, "6. Agent Responsibilities")
    agents = [
        ("Bug Detector", "Inspects source code using regex-based pattern matching. "
         "Identifies suspicious patterns (missing boundary checks, absent state "
         "transitions) and classifies the bug with type, severity, and confidence."),
        ("Root Cause Analyser", "Explains why the detected bug occurs by tracing "
         "the relevant function and control flow. Identifies the specific faulty "
         "condition and recommends a minimal corrective change."),
        ("Fix Generator", "Produces a minimal string-replacement patch targeting "
         "the identified root cause. Generates a unified diff for review. Never "
         "modifies the original source file."),
        ("Test Verifier", "Copies the project to an isolated temporary directory. "
         "Runs pytest before (baseline) and after (post-fix) applying the patch. "
         "Returns structured pass/fail results with captured output."),
        ("Decision Agent", "Evaluates test results using deterministic rules. "
         "Routes to success if tests pass, retry if attempts remain, or human "
         "review if retries are exhausted or a safety concern exists."),
    ]
    for name, desc in agents:
        _add_heading(doc, f"6.{agents.index((name, desc))+1} {name}", level=2)
        _add_para(doc, desc)

    # ── Demo Bugs ────────────────────────────────────────
    _add_heading(doc, "7. Sample Game Bugs")
    bugs = [
        ("BUG-001: Player Health Can Become Negative",
         "game_project/player.py", "Player.take_damage",
         "Health is reduced without a lower-bound clamp.",
         "self.health = max(0, self.health - amount)"),
        ("BUG-002: Inventory Exceeds Maximum Capacity",
         "game_project/inventory.py", "Inventory.add_item",
         "Items are appended without checking capacity.",
         "if len(self.items) >= self.capacity: return False"),
        ("BUG-003: Enemy AI State Does Not Reset",
         "game_project/enemy_ai.py", "EnemyAI.update",
         "Missing else branch to reset state to IDLE.",
         "else: self.state = self.IDLE"),
    ]
    for title, file, func, issue, fix in bugs:
        _add_heading(doc, title, level=2)
        _add_para(doc, f"File: {file}\nFunction: {func}\nIssue: {issue}\nFix: {fix}")

    # ── Testing ──────────────────────────────────────────
    _add_heading(doc, "8. Testing Methodology & Results")
    _add_para(doc,
        "The test suite consists of 22 tests across 4 test files:\n\n"
        "• test_health.py (6 tests): 2 fail on buggy code, 4 regression tests\n"
        "• test_inventory.py (5 tests): 1 fails on buggy code, 4 regression tests\n"
        "• test_enemy_ai.py (5 tests): 1 fails on buggy code, 4 regression tests\n"
        "• test_workflow.py (6 tests): full pipeline integration tests\n\n"
        "Results:\n"
        "• Game tests against buggy code: 4 FAILED, 12 PASSED (confirms bugs exist)\n"
        "• Pipeline integration tests: 6 PASSED (confirms fixes work)\n"
        "• All tests pass after patches are applied in isolated temp directories\n"
        "• Original source files remain unchanged after pipeline execution"
    )

    # ── Safety ───────────────────────────────────────────
    _add_heading(doc, "9. Patch Safety & Human-in-the-Loop Design")
    _add_para(doc,
        "Safety is implemented at multiple levels:\n\n"
        "• Patches are applied only to temporary copies of source files.\n"
        "• Original project files are never modified by the pipeline.\n"
        "• Tests run in a subprocess with a 30-second timeout.\n"
        "• No arbitrary shell commands are executed.\n"
        "• Path traversal in patch targets is not possible.\n"
        "• The Decision Agent uses deterministic rules for safety-critical routing.\n"
        "• Failed fixes are retried up to a configurable maximum.\n"
        "• Unresolved cases are escalated to human review.\n\n"
        "Note: This is a controlled proof of concept, not a fully sandboxed "
        "production security system."
    )

    # ── Limitations ──────────────────────────────────────
    _add_heading(doc, "10. Limitations")
    limitations = [
        "Deterministic agents only — no real LLM integration in the demo.",
        "Handles predefined bug patterns; not generalised to arbitrary bugs.",
        "Single-file patches only; no multi-file support.",
        "No real game engine integration.",
        "Not a production security sandbox.",
        "Confidence scores are demonstration values, not statistically validated.",
    ]
    for lim in limitations:
        doc.add_paragraph(lim, style="List Bullet")

    # ── Future Scope ─────────────────────────────────────
    _add_heading(doc, "11. Future Scope")
    futures = [
        "LLM-powered bug detection and patch generation with schema validation.",
        "Support for multiple programming languages and game engines.",
        "Multi-file and cross-module patch generation.",
        "Persistent audit logs and review decision tracking.",
        "Configurable risk policies and approval workflows.",
        "Integration with CI/CD pipelines for automated regression testing.",
        "Visual diff viewer with syntax highlighting.",
        "PDF/image bug report support with OCR.",
    ]
    for f in futures:
        doc.add_paragraph(f, style="List Bullet")

    # ── Conclusion ───────────────────────────────────────
    _add_heading(doc, "12. Conclusion")
    _add_para(doc,
        "This proof of concept successfully demonstrates that agentic AI, "
        "orchestrated through LangGraph, can effectively structure the game-"
        "debugging workflow into specialised, coordinated agents. The pipeline "
        "detects all three demo bugs with high confidence, generates correct "
        "patches, verifies them through automated testing, and routes results "
        "through conditional logic including retry loops and human-review "
        "escalation. The system runs without any API key, uses safe patch "
        "application practices, and provides transparent results through an "
        "interactive Streamlit interface."
    )

    # ── References ───────────────────────────────────────
    _add_heading(doc, "References")
    refs = [
        "LangGraph Documentation — https://langchain-ai.github.io/langgraph/",
        "Streamlit Documentation — https://docs.streamlit.io/",
        "pytest Documentation — https://docs.pytest.org/",
        "Python Documentation — https://docs.python.org/3/",
    ]
    for ref in refs:
        doc.add_paragraph(ref, style="List Bullet")

    out = _ROOT / "docs" / "Project_Report.docx"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print(f"✅ Saved: {out}")


# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    generate_pptx()
    generate_docx()
    print("\n✅ All documents generated successfully.")
