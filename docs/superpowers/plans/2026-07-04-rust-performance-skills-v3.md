# Rust Performance Skills V3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add industrial Rust quality gates, verification guidance, release engineering, CI templates, eval scenarios, richer project audit, quality gate generation, and a one-line installer.

**Architecture:** Extend the current skill-first distribution with three operational skills and deterministic scripts. Use tests to define the required outputs before implementation. Keep templates copyable and scripts dependency-free.

**Tech Stack:** Markdown skills, shell installer, Python standard library scripts/tests, GitHub Actions YAML templates.

---

### Task 1: Add Red Tests For V3 Distribution

**Files:**
- Modify: `tests/test_distribution.py`
- Create: `tests/test_installer_contract.py`

- [ ] Require the three new skill folders and metadata.
- [ ] Require CI templates, eval scenarios, and `install.sh`.
- [ ] Verify the README contains the one-liner install command.
- [ ] Run distribution tests and confirm they fail on missing v3 artifacts.

### Task 2: Add Red Tests For Audit And Quality Gate Generation

**Files:**
- Modify: `tests/test_rust_project_audit.py`
- Create: `tests/test_generate_quality_gates.py`
- Create: `scripts/generate_quality_gates.py`

- [ ] Require audit detection for workspace, lockfile, cargo-deny, nextest, fuzz, coverage, semver, and Miri suitability.
- [ ] Require generator output for Rust, PyO3, Wasm, unsafe, and HFT projects.
- [ ] Run tests and confirm they fail before implementation.

### Task 3: Implement V3 Skills And References

**Files:**
- Create: `skills/rust-ci-quality-gates/*`
- Create: `skills/rust-testing-verification/*`
- Create: `skills/rust-crate-release-engineering/*`
- Modify: `skills/rust-performance-engineering/SKILL.md`
- Modify: `skills/rust-review-auditor/SKILL.md`

- [ ] Implement skill entrypoints and references.
- [ ] Add `agents/openai.yaml` for each new skill.
- [ ] Route the new skills from the main router and review auditor.

### Task 4: Implement Scripts, Installer, Templates, Evals, Docs

**Files:**
- Create: `install.sh`
- Create: `scripts/generate_quality_gates.py`
- Modify: `scripts/rust_project_audit.py`
- Modify: `scripts/validate_distribution.py`
- Create: `templates/ci/*.yml`
- Create: `evals/*.md`
- Modify: `README.md`
- Modify: `docs/install/*.md`
- Modify: `docs/sources.md`

- [ ] Implement the one-line installer.
- [ ] Implement richer audit and gate generation.
- [ ] Add CI templates and eval prompts.
- [ ] Update docs and source map.

### Task 5: Verify, Commit, Merge, Push

**Files:**
- All changed files.

- [ ] Run `python3 -m unittest discover -s tests`.
- [ ] Run `python3 scripts/validate_distribution.py`.
- [ ] Run official plugin validator.
- [ ] Run official skill validator on every skill.
- [ ] Commit as `feat: add industrial rust quality gates v3`.
- [ ] Merge into `main`, push, and verify GitHub Actions.
