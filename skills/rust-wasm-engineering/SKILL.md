---
name: rust-wasm-engineering
description: "Use when compiling Rust to WebAssembly or designing Wasm packages: wasm-bindgen, wasm-pack-style builds, browser or Node targets, JS boundary cost, memory transfer, typed arrays, code size, wasm-opt, panic strategy, profiling, TypeScript bindings, and frontend performance."
---

# Rust Wasm Engineering

Use this skill when Rust runs as WebAssembly. Load `references/wasm-engineering.md` for details.

## Workflow

1. Confirm why Wasm is needed: CPU-heavy work, deterministic runtime, reuse of Rust code, or boundary isolation.
2. Design a coarse-grained JS/Wasm API to avoid per-item boundary crossings.
3. Choose target: browser, bundler, Node, web worker, or no-bindgen runtime.
4. Tune for size and performance separately.
5. Measure generated Wasm, generated JS, load time, and runtime hot path.

## Output

Include target, boundary design, memory transfer strategy, build profile, size optimization plan, and benchmark plan.
