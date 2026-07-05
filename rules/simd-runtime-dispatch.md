# simd-runtime-dispatch

## id
simd-runtime-dispatch

## severity
high

## trigger
SIMD acceleration using core::arch, std::simd, target_feature, or CPU-specific hot paths.

## bad
```rust
#[target_feature(enable = "avx2")]
unsafe fn sum_avx2(xs: &[f32]) -> f32 {
    simd_sum(xs)
}
```

## good
```rust
fn sum(xs: &[f32]) -> f32 {
    if is_x86_feature_detected!("avx2") {
        unsafe { sum_avx2(xs) }
    } else {
        sum_scalar(xs)
    }
}
```

## when
Use when profiling shows vectorizable arithmetic, parsing, scanning, or transform work in a hot path.

## when_not
Do not require a CPU feature unless deployment is pinned to that CPU class or a scalar fallback exists.

## verification
Measure scalar fallback, CPU feature gates, alignment assumptions, tail handling, and per-target benchmark results.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- core::arch docs: https://doc.rust-lang.org/core/arch/

## related_rules
- opt-simd-portable
- unsafe-minimize-scope
- num-overflow-explicit
