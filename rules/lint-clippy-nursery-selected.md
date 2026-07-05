# lint-clippy-nursery-selected

## id
lint-clippy-nursery-selected

## severity
low

## trigger
Enable high-value `clippy::nursery` lints selectively, not the whole group. Trigger when working on linting and the code shows `lint`-class risk.

## bad
```toml
# Cargo.toml - enables every nursery lint, including noisy ones
[lints.clippy]
nursery = "warn"
```

## good
```toml
# Cargo.toml - selectively enable high-value nursery lints
[lints.clippy]
# Catches lock/guard held longer than necessary (overlaps with async issues)
significant_drop_tightening = "warn"
# Flags .clone() calls that could be avoided by moving
redundant_clone = "warn"
# Replace TypeName with Self inside impl blocks
use_self = "warn"
# Avoid redundant else after a diverging if
redundant_else = "warn"
# Prefer or_default() over or(Default::default())
or_fun_call = "warn"
```

```rust
// significant_drop_tightening example - lint fires here:
fn process(state: &Mutex<Vec<u32>>) -> usize {
    let guard = state.lock().unwrap();
    let len = guard.len();
    drop(guard);          // lint suggests dropping earlier, before the return
    expensive_work();
    len
}

// use_self example - lint fires here:
impl MyStruct {
    fn new() -> MyStruct {   // should be -> Self
        MyStruct { value: 0 }
    }
}

// Correct:
impl MyStruct {
    fn new() -> Self {
        Self { value: 0 }
    }
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Run cargo clippy with the intended lint level and document any allow with a narrow reason.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- anti-lock-across-await
- lint-pedantic-selective
- lint-warn-perf
