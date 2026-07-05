# closure-fn-trait-bounds

## id
closure-fn-trait-bounds

## severity
medium

## trigger
Require the least restrictive `Fn` trait a callback needs (`FnOnce` superset-or-equal `FnMut` superset-or-equal `Fn`). Trigger when working on closures and callbacks and the code shows `closure`-class risk.

## bad
```rust
// F: Fn is too strict - the closure is only called once,
// so move-consuming closures are unnecessarily rejected.
fn run_once_bad<F: Fn() -> String>(f: F) -> String {
    f()
}

fn demo_bad() {
    let s = String::from("hello");
    // This closure consumes `s`, so it only implements FnOnce, not Fn.
    // run_once_bad(move || s) // compile error: `s` moved in closure
    let _ = run_once_bad(|| String::from("ok")); // forced to use non-consuming closure
}
```

## good
```rust
// Use FnOnce when you call the closure exactly once.
fn run_once<F: FnOnce() -> String>(f: F) -> String {
    f()
}

// Use FnMut when you call the closure multiple times and it may mutate state.
fn retry<F: FnMut() -> bool>(mut f: F, attempts: usize) -> bool {
    for _ in 0..attempts {
        if f() {
            return true;
        }
    }
    false
}

// Use Fn when you call the closure multiple times and need it shareable/re-entrant.
fn for_each<T, F: Fn(&T)>(items: &[T], f: F) {
    for item in items {
        f(item);
    }
}

fn demo() {
    // FnOnce: move-consuming closure is accepted
    let s = String::from("hello");
    let result = run_once(move || s.to_uppercase());
    assert_eq!(result, "HELLO");

    // FnMut: closure mutates a counter
    let mut count = 0usize;
    let found = retry(
        || {
            count += 1;
            count == 3
        },
        5,
    );
    assert!(found);

    // Fn: read-only closure, called once per element
    let nums = vec![1, 2, 3];
    for_each(&nums, |n| println!("{n}"));
}
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
- closure-move-capture
- closure-static-vs-dyn
