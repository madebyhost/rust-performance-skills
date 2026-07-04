# Rust Performance Core Reference

## Measurement

- Use Criterion for statistical microbenchmarks.
- Use flamegraphs or `perf` for CPU hotspots.
- Use heap profilers or allocation counters for allocation pressure.
- Keep representative inputs and release-mode builds.

## Cargo Profiles

Inspect:

```toml
[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
debug = "line-tables-only"
strip = "symbols"
```

These settings trade build time, debuggability, binary size, and runtime speed. Do not apply them blindly.

## Hot Path Tactics

- Replace repeated indexing with iterators or slices when it removes bounds checks.
- Preallocate `Vec`, `String`, and buffers when bounds are known.
- Split hot and cold fields.
- Prefer contiguous data and predictable access.
- Avoid formatting/logging in inner loops.
- Benchmark hashing choices for hash-heavy paths.

## Red Flags

- benchmark in debug mode;
- optimizing without profiling;
- `clone`, `to_string`, or `collect` inside hot loops;
- `HashMap` for tiny fixed sets;
- `LinkedList` for performance;
- stripping symbols before profiling.
