# Source Map

This project turns stable Rust ecosystem guidance into agent workflows. Prefer primary or official sources when updating skills.

## Rust Quality And Performance

- The Rust Performance Book: https://nnethercote.github.io/perf-book/
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/
- Rust Design Patterns: https://rust-unofficial.github.io/patterns/
- Rust 2024 Edition Guide: https://doc.rust-lang.org/edition-guide/rust-2024/
- Cargo profiles: https://doc.rust-lang.org/cargo/reference/profiles.html
- Clippy lints: https://doc.rust-lang.org/clippy/lints.html
- Criterion.rs: https://bheisler.github.io/criterion.rs/book/
- cargo-nextest: https://nexte.st/
- cargo-deny: https://embarkstudios.github.io/cargo-deny/
- cargo-audit: https://rustsec.org/
- cargo-semver-checks: https://github.com/obi1kenobi/cargo-semver-checks
- Miri: https://github.com/rust-lang/miri/
- cargo-fuzz: https://rust-fuzz.github.io/book/cargo-fuzz.html
- cargo-llvm-cov: https://crates.io/crates/cargo-llvm-cov
- cargo-mutants: https://mutants.rs/

## Comparative Rust Skill Corpora

- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- actionbook/rust-skills: https://github.com/actionbook/rust-skills
- MCP Market rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit rust-best-practices: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Local comparison notes: docs/third-party-rust-skills-review.md
- Local MCPMarket review notes: docs/mcpmarket-rust-best-practices-review.md

## Multi-Agent Install Surfaces

- RTK init target list: `rtk init --help`
- Claude Code plugin creation: https://code.claude.com/docs/en/plugins
- Claude Code plugin marketplaces: https://code.claude.com/docs/en/plugin-marketplaces
- Claude Code plugin discovery and disable flow: https://code.claude.com/docs/en/discover-plugins
- Hermes configuration and skills directory: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- OpenClaw configuration and skills config: https://docs.openclaw.ai/gateway/configuration
- Ollama OpenClaw integration: https://docs.ollama.com/integrations/openclaw

## Rust Expert Rulebook

- Local rule cards: rules/
- Rule index: rules/index.json
- Importer: scripts/import_leonardomso_rules.py
- Rule schema: id, severity, trigger, bad, good, when, when_not, verification, sources, related_rules
- Imported base: leonardomso/rust-skills under the repository MIT license, normalized into local expert rule cards.
- Local extensions: rust-performance-skills rules for HFT, SBE, eBPF, PyO3, Wasm, Tauri, SIMD, NUMA, graph/math kernels, and io_uring.
- MCPMarket review extensions: rust-best-practices guidance normalized into stronger local rules for async runtime selection, blocking boundaries, constructor ownership, fallible iterator collection, boolean API modes, early-return readability, named constants, and local quality gates.

## Kernel And eBPF

- Linux BPF documentation: https://docs.kernel.org/bpf/
- docs.ebpf.io: https://docs.ebpf.io/
- ebpf.io: https://ebpf.io/
- Aya: https://aya-rs.dev/
- libbpf-rs: https://github.com/libbpf/libbpf-rs

## Binary Encoding

- FIX SBE: https://github.com/FIXTradingCommunity/fix-simple-binary-encoding
- Real Logic SBE: https://real-logic.github.io/simple-binary-encoding/

## Math And Algorithms

- petgraph: https://docs.rs/petgraph/latest/petgraph/
- ndarray: https://docs.rs/ndarray/latest/ndarray/
- Rayon: https://docs.rs/rayon/latest/rayon/
- rand: https://docs.rs/rand/latest/rand/
- rand_distr: https://docs.rs/rand_distr/latest/rand_distr/
- statrs: https://docs.rs/statrs/latest/statrs/
- Rust std SIMD: https://doc.rust-lang.org/std/simd/

## Memory SIMD And I/O

- Rust core::arch SIMD intrinsics: https://doc.rust-lang.org/core/arch/
- Rust std::simd portable SIMD: https://doc.rust-lang.org/std/simd/
- memmap2: https://docs.rs/memmap2/
- io-uring: https://docs.rs/io-uring/latest/io_uring/
- io_uring manual pages: https://man7.org/linux/man-pages/man7/io_uring.7.html
- mimalloc: https://docs.rs/mimalloc/
- tikv-jemallocator: https://docs.rs/tikv-jemallocator/
- bumpalo: https://docs.rs/bumpalo/latest/bumpalo/
- bytemuck: https://docs.rs/bytemuck/
- zerocopy: https://docs.rs/zerocopy/latest/zerocopy/
- Linux HugeTLB documentation: https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt
- Linux NUMA memory policy: https://man7.org/linux/man-pages/man2/set_mempolicy.2.html

## Unsafe And FFI

- The Rustonomicon: https://doc.rust-lang.org/nomicon/
- Rustonomicon FFI chapter: https://doc.rust-lang.org/nomicon/ffi.html
- bindgen user guide: https://rust-lang.github.io/rust-bindgen/

## Python Bindings

- PyO3 user guide: https://pyo3.rs/
- PyO3 performance: https://pyo3.rs/main/performance
- PyO3 parallelism: https://pyo3.rs/v0.29.0/parallelism
- PyO3 free-threading: https://pyo3.rs/v0.29.0/free-threading
- maturin user guide: https://www.maturin.rs/

## WebAssembly

- Rust and WebAssembly: https://rustwasm.github.io/book/
- wasm-bindgen guide: https://rustwasm.github.io/docs/wasm-bindgen/
- Rust WebAssembly overview: https://www.rust-lang.org/what/wasm/

## Tauri Desktop And Mobile Apps

- Tauri v2: https://v2.tauri.app/start/
- Tauri process model: https://v2.tauri.app/concept/process-model/
- Tauri IPC: https://v2.tauri.app/concept/inter-process-communication/
- Tauri app size: https://v2.tauri.app/concept/size/
- Tauri mobile prerequisites: https://v2.tauri.app/start/prerequisites/
- Tauri distribution: https://v2.tauri.app/distribute/
- Tauri Rust to frontend communication: https://v2.tauri.app/develop/calling-frontend/
- Tauri configuration files: https://v2.tauri.app/develop/configuration-files/
