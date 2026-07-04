# Rust Performance Skills V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the plugin into a multi-skill Rust performance engineering distribution with deterministic validation and project audit tooling.

**Architecture:** Keep `rust-performance-engineering` as the router. Add focused skill folders with concise `SKILL.md` entrypoints and reference files. Add Python tests first for distribution requirements and the project audit script, then implement the skills/scripts until tests pass.

**Tech Stack:** Markdown skills, Codex plugin JSON, Python standard library tests, GitHub Actions.

---

### Task 1: Add Red Tests For V2 Distribution

**Files:**
- Create: `tests/test_distribution.py`
- Modify: `scripts/validate_distribution.py`

- [ ] Add tests that require the v2 skill list, `agents/openai.yaml`, router links, install docs, and no placeholder text.
- [ ] Run `python3 -m unittest tests/test_distribution.py` and verify it fails because the v2 skills do not exist yet.

### Task 2: Add Red Tests For Rust Project Audit

**Files:**
- Create: `tests/test_rust_project_audit.py`
- Create: `scripts/rust_project_audit.py`

- [ ] Add tests for missing `Cargo.toml`, release profile findings, PyO3/maturin detection, Wasm detection, unsafe signal detection, and HFT signal detection.
- [ ] Run `python3 -m unittest tests/test_rust_project_audit.py` and verify it fails because the audit implementation is absent.

### Task 3: Implement V2 Skills

**Files:**
- Modify: `skills/rust-performance-engineering/SKILL.md`
- Create: `skills/rust-code-quality/SKILL.md`
- Create: `skills/rust-performance-core/SKILL.md`
- Create: `skills/rust-async-concurrency/SKILL.md`
- Create: `skills/rust-low-latency-hft/SKILL.md`
- Create: `skills/rust-python-pyo3-maturin/SKILL.md`
- Create: `skills/rust-wasm-engineering/SKILL.md`
- Create: `skills/rust-ffi-bindings/SKILL.md`
- Create: `skills/rust-unsafe-soundness/SKILL.md`
- Create: `skills/rust-architecture-patterns/SKILL.md`
- Create: `skills/rust-review-auditor/SKILL.md`
- Create: matching `agents/openai.yaml` files and references.

- [ ] Implement each skill as a focused entrypoint with routing and review outputs.
- [ ] Add reference files for detailed guidance and source-backed checklists.

### Task 4: Implement Scripts And CI

**Files:**
- Modify: `scripts/validate_distribution.py`
- Create: `scripts/rust_project_audit.py`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `docs/install/*.md`
- Create: `docs/sources.md`

- [ ] Implement validation against all v2 skills.
- [ ] Implement the project audit CLI.
- [ ] Extend CI to run unit tests and distribution validation.
- [ ] Update docs to describe the multi-skill architecture and audit script.

### Task 5: Verify And Publish

**Files:**
- All changed files.

- [ ] Run `python3 -m unittest`.
- [ ] Run `python3 scripts/validate_distribution.py`.
- [ ] Run official skill and plugin validators.
- [ ] Commit as `feat: expand rust performance skills v2`.
- [ ] Merge to `main`, push, and verify GitHub Actions.
