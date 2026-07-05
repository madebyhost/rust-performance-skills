# Rust Performance Skills V5 Kernel Codecs Math Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add eBPF/kernel, SBE/binary-codec, and math/algorithm performance specialization to the Rust Performance Skills plugin and MCP.

**Architecture:** Add three concise specialist skills with reference files and OpenAI UI metadata. Extend static audit and MCP logic with deterministic signal detection and checklists. Keep install/plugin behavior unchanged and keep MCP offline.

**Tech Stack:** Codex skills, Python standard library, unittest, Markdown references.

---

## File Structure

- Create `skills/rust-ebpf-kernel-performance/` with `SKILL.md`, `agents/openai.yaml`, and `references/ebpf-kernel-performance.md`.
- Create `skills/rust-sbe-binary-codecs/` with `SKILL.md`, `agents/openai.yaml`, and `references/sbe-binary-codecs.md`.
- Create `skills/rust-math-algorithms-performance/` with `SKILL.md`, `agents/openai.yaml`, and `references/math-algorithms-performance.md`.
- Modify `skills/rust-performance-engineering/SKILL.md`, `skills/rust-review-auditor/SKILL.md`, and `skills/rust-low-latency-hft/SKILL.md`.
- Modify `scripts/rust_project_audit.py` and `mcp/rust_performance_mcp.py`.
- Modify `tests/test_distribution.py`, `tests/test_rust_project_audit.py`, `tests/test_mcp_contract.py`, and `scripts/validate_distribution.py`.
- Modify `README.md` and `docs/sources.md`.
- Create `evals/ebpf-xdp-kernel.md`, `evals/sbe-market-data-codec.md`, and `evals/math-graph-simulation.md`.

## Tasks

### Task 1: Distribution Tests For New Skills And Sources

- [ ] Add failing assertions in `tests/test_distribution.py` for the three new skill folders, eval files, and source tokens: `docs.ebpf.io`, `ebpf.io`, `Aya`, `libbpf-rs`, `FIX SBE`, `Real Logic SBE`, `petgraph`, `ndarray`, `Rayon`, `rand_distr`, `statrs`.
- [ ] Run `python3 -m unittest tests.test_distribution -v` and verify it fails because files/tokens do not exist.
- [ ] Create the three skill directories with concise `SKILL.md`, `agents/openai.yaml`, and references.
- [ ] Update router/review/HFT skills, README, docs/sources.md, eval files, and `scripts/validate_distribution.py`.
- [ ] Run `python3 -m unittest tests.test_distribution -v` and `python3 scripts/validate_distribution.py`; both must pass.
- [ ] Commit with `feat: add kernel codec math performance skills`.

### Task 2: Audit Detection

- [ ] Add failing tests in `tests/test_rust_project_audit.py` for eBPF, SBE, and math/algorithm fixtures.
- [ ] Run `python3 -m unittest tests.test_rust_project_audit -v` and verify expected failures.
- [ ] Extend `scripts/rust_project_audit.py` with dependency/source signal regexes and recommendations for eBPF, SBE, and math/algorithm domains.
- [ ] Run `python3 -m unittest tests.test_rust_project_audit -v`; it must pass.
- [ ] Commit with `feat: detect ebpf sbe math rust signals`.

### Task 3: MCP Tools

- [ ] Add failing tests in `tests/test_mcp_contract.py` for `detect_performance_domains`, `rust_algorithm_checklist`, and `binary_encoding_review_checklist`.
- [ ] Run `python3 -m unittest tests.test_mcp_contract -v` and verify expected failures.
- [ ] Extend `mcp/rust_performance_mcp.py` tool metadata and direct call logic; update `rust_review_checklist` to include eBPF/SBE/math checks when signals are present.
- [ ] Run `python3 -m unittest tests.test_mcp_contract -v`; it must pass.
- [ ] Commit with `feat: extend mcp performance domain tools`.

### Task 4: Full Verification And Push

- [ ] Run `python3 -m unittest discover -s tests`.
- [ ] Run `python3 scripts/validate_distribution.py`.
- [ ] Run plugin validation with `/tmp/rust-performance-skills-venv/bin/python /Users/admin/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /Users/admin/Documents/Codex/2026-07-04/a/work/rust-performance-skills`.
- [ ] Run skill validation with `zsh -lc 'for d in skills/*; do /tmp/rust-performance-skills-venv/bin/python /Users/admin/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$d" || exit 1; done'`.
- [ ] Run `sh -n install.sh` and `python3 mcp/rust_performance_mcp.py --list-tools`.
- [ ] Verify no private project metadata appears in committed files.
- [ ] Fast-forward `main`, push, watch GitHub Actions, and confirm authors are `Mehdi AISSANI <contact@mehdiaissani.com>`.
