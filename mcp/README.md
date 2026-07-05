# Rust Performance MCP

This repository remains skill-first, but it includes an offline stdio MCP server for deterministic tasks that should not depend on model memory.

Current tools:

- `audit_rust_project`: inspect Rust project structure and performance signals.
- `generate_quality_gates`: produce quality-gate commands from an audit.
- `list_rust_skills`: list packaged specialist skills.
- `rust_review_checklist`: produce review checks from project findings.
- `detect_performance_domains`: classify detected Rust performance domains.
- `rust_algorithm_checklist`: return graph, stochastic, and numerical performance checks.
- `binary_encoding_review_checklist`: return SBE and binary-codec checks.
- `memory_simd_io_checklist`: return allocator, SIMD, mmap, io_uring, NUMA, and zero-copy checks.
- `api_type_design_checklist`: return API/type-system, serde, macro, cfg, and semver checks.
- `tauri_app_checklist`: return Tauri desktop/mobile IPC, channels, bundle, signing, system webview, and security checks.
- `select_rust_rules`: select concrete rule cards from `rules/index.json`.
- `explain_rust_rule`: return one full rule card with bad/good examples and verification.

Keep architectural judgment in the skills. Use MCP tools for selection, indexing, repeatable checks, and structured context.
