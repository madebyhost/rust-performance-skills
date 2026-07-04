# Rust Performance Skills V3 Design

## Goal

Make `rust-performance-skills` industrial-grade by adding quality gates, verification strategy, release engineering, CI templates, a one-line installer, richer Rust project audit, quality gate generation, and evaluation scenarios.

## Architecture

Keep the repository skill-first. Add three specialist skills for operational quality: `rust-ci-quality-gates`, `rust-testing-verification`, and `rust-crate-release-engineering`. Add templates and scripts that turn the guidance into concrete outputs agents can apply to real projects.

The installer stays shell-based and portable. It supports a one-liner from GitHub and copies all skill folders into common local agent skill directories. It must not require privileged access.

## Components

- `skills/rust-ci-quality-gates`: nextest, clippy, fmt, cargo-deny, RustSec/cargo-audit, cargo-semver-checks, CI quality gates.
- `skills/rust-testing-verification`: unit/integration/property tests, Miri, cargo-fuzz, cargo-llvm-cov, cargo-mutants.
- `skills/rust-crate-release-engineering`: MSRV, semver, feature flags, docs.rs, workspace hygiene, release profiles.
- `templates/ci/`: GitHub Actions templates for Rust library, PyO3/maturin, Wasm, and HFT/perf projects.
- `install.sh`: one-line installer for Codex, Claude, and generic local skill directories.
- `scripts/generate_quality_gates.py`: emits recommended CI and verification commands from audit signals.
- `scripts/rust_project_audit.py`: enriched to detect workspaces, lockfiles, deny config, nextest config, fuzz targets, coverage setup, semver risk, Miri suitability, and release engineering signals.
- `evals/`: scenario prompts for Rust quality, PyO3, Wasm, HFT, unsafe, async, and release review.

## One-Line Install

The public install command is:

```bash
curl -fsSL https://raw.githubusercontent.com/madebyhost/rust-performance-skills/main/install.sh | sh
```

Optional environment variables:

- `RUST_PERF_SKILLS_TARGET=all|codex|claude|local`
- `RUST_PERF_SKILLS_PREFIX=/custom/path`
- `RUST_PERF_SKILLS_REF=main`

## Validation

The v3 is complete when:

- all new skills validate;
- distribution tests require the new skills, templates, installer, and evals;
- audit tests cover the new detections;
- quality gate generator tests cover Rust, PyO3, Wasm, unsafe, and HFT output;
- `python3 -m unittest discover -s tests`, `scripts/validate_distribution.py`, official plugin validation, and official skill validation pass;
- GitHub Actions passes after push.
