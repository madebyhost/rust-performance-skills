# Rust Performance Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a portable Rust performance skill distribution with Codex plugin support.

**Architecture:** Create a skill-first repository with Codex plugin metadata, reference playbooks, install docs, and validation CI. Keep MCP as a future extension point so v1 stays immediately usable across agents.

**Tech Stack:** Markdown skills, Codex plugin JSON, Python validation, GitHub Actions.

---

### Task 1: Repository Skeleton

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `.mcp.json`
- Create: `README.md`
- Create: `LICENSE`
- Create: `CONTRIBUTING.md`

- [x] Create Codex plugin metadata with name `rust-performance-skills`.
- [x] Add open-source README and MIT license.
- [x] Keep `.mcp.json` valid while leaving MCP servers empty for v1.

### Task 2: Main Skill

**Files:**
- Create: `skills/rust-performance-engineering/SKILL.md`
- Create: `skills/rust-performance-engineering/agents/openai.yaml`

- [x] Define skill frontmatter with broad Rust performance triggers.
- [x] Add measurement-first workflow.
- [x] Route detailed topics to reference files.

### Task 3: References

**Files:**
- Create: `skills/rust-performance-engineering/references/measurement.md`
- Create: `skills/rust-performance-engineering/references/zero-copy.md`
- Create: `skills/rust-performance-engineering/references/async-concurrency.md`
- Create: `skills/rust-performance-engineering/references/low-latency-hft.md`
- Create: `skills/rust-performance-engineering/references/data-layout-memory.md`
- Create: `skills/rust-performance-engineering/references/architecture.md`
- Create: `skills/rust-performance-engineering/references/review-checklists.md`

- [x] Add practical guidance for each performance domain.
- [x] Include red flags and verification expectations.

### Task 4: Install Docs And CI

**Files:**
- Create: `docs/install/codex.md`
- Create: `docs/install/claude.md`
- Create: `docs/install/generic-agents.md`
- Create: `scripts/validate_distribution.py`
- Create: `.github/workflows/ci.yml`

- [x] Document install routes for Codex, Claude, and generic agents.
- [x] Add Python validation for plugin JSON, skill frontmatter, reference links, and required docs.
- [x] Run validation locally before publishing.
