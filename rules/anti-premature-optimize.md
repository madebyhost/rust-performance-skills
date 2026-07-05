# anti-premature-optimize

## id
anti-premature-optimize

## severity
reference

## trigger
Don't optimize before profiling. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// "Optimizing" without measurement
fn sum(data: &[i32]) -> i32 {
    // Using unsafe "for performance" without profiling
    unsafe {
        let mut sum = 0;
        for i in 0..data.len() {
            sum += *data.get_unchecked(i);
        }
        sum
    }
}

// Complex caching with no evidence it's needed
lazy_static! {
    static ref CACHE: RwLock<HashMap<String, Arc<Result>>> =
        RwLock::new(HashMap::new());
}

// Hand-rolled data structures "for speed"
struct MyVec<T> {
    ptr: *mut T,
    len: usize,
    cap: usize,
}
```

## good
```rust
// Simple, idiomatic - let compiler optimize
fn sum(data: &[i32]) -> i32 {
    data.iter().sum()
}

// Profile, then optimize if needed
fn sum_optimized(data: &[i32]) -> i32 {
    // After profiling showed this is a bottleneck,
    // we measured that manual SIMD gives 3x speedup
    #[cfg(target_arch = "x86_64")]
    {
        // a hand-written SIMD path would go here (measured ~3x faster);
        // fall back to the iterator version as a placeholder
        data.iter().sum()
    }
    #[cfg(not(target_arch = "x86_64"))]
    {
        data.iter().sum()
    }
}

// Use standard library - it's well-optimized
let cache: HashMap<String, Result> = HashMap::new();
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Add focused tests or static checks that prove the intended behavior and prevent regression.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- opt-inline-small
- perf-profile-first
- test-criterion-bench
