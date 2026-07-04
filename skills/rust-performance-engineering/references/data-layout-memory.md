# Data Layout And Memory

Data layout is often the real Rust performance lever.

## Allocation Control

- Preallocate with `Vec::with_capacity` when the bound is known.
- Reuse scratch buffers across calls.
- Use arenas for batch-lifetime allocations.
- Use `SmallVec` or `ArrayVec` when small fixed upper bounds are real and measured.
- Avoid per-message `Box`, `String`, or `Vec` in hot paths.

## Arrays, Vecs, And Slices

- Fixed arrays are useful for small known sizes and stack/locality benefits.
- `Vec<T>` is appropriate for dynamic contiguous storage.
- Prefer slices in APIs: `&[T]`, `&mut [T]`.
- Avoid `Vec<Box<T>>` in hot paths unless stable addresses or trait objects are required.

## Cache Locality

- Use AoS when most operations touch most fields of each record.
- Use SoA when scans touch one or two fields across many records.
- Split hot and cold fields.
- Keep frequently accessed state compact.
- Avoid pointer chasing in inner loops.

## False Sharing

- Separate contended atomics or counters onto different cache lines.
- Use padding wrappers intentionally and document why.
- Beware arrays of per-thread counters packed next to each other.

## Red Flags

- many small allocations per request or message;
- `HashMap` in an innermost loop where indexes or arrays would work;
- cold metadata stored inside hot structs;
- clone-heavy transformations between near-identical DTOs;
- generic collections chosen before access patterns are known.

## Verification

- Inspect allocation counts.
- Use cache-miss profiles where available.
- Benchmark realistic cardinalities and input distributions.
- Test with production-like struct sizes and feature flags.
