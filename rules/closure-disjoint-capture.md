# closure-disjoint-capture

## id
closure-disjoint-capture

## severity
medium

## trigger
Capture only what you use; lean on edition-2021 disjoint closure captures. Trigger when working on closures and callbacks and the code shows `closure`-class risk.

## bad
```rust
struct Config {
    threshold: i32,
    label: String,
}

fn demo_bad() {
    let config = Config { threshold: 10, label: String::from("demo") };

    // In pre-2021 editions the whole `config` is captured, blocking access
    // to `config.label` below. In 2021 this compiles, but the pattern of
    // capturing the whole struct via `move` is the real footgun:
    let threshold = config.threshold; // copy out the field first
    let check = move || threshold > 0; // now `config` is NOT fully moved

    // If instead you wrote: let check = move || config.threshold > 0;
    // `config` would be moved in, making `config.label` inaccessible afterwards.
    // Demonstrate the problematic pattern (commented out to allow compilation):
    // let check2 = move || config.threshold > 0;
    // println!("{}", config.label); // error: use of moved value

    println!("label still accessible: {}", config.label);
    assert!(check());
}
```

## good
```rust
struct Config {
    threshold: i32,
    label: String,
}

fn demo_good() {
    let config = Config { threshold: 10, label: String::from("active") };

    // Edition 2021: the closure captures only `config.threshold` (a Copy field).
    // `config.label` is NOT captured, so it remains accessible.
    let check = || config.threshold > 0;

    // Both are usable simultaneously.
    println!("label: {}", config.label);  // fine - not captured by `check`
    assert!(check());
}

// When you need `move` for one field, bind it first.
fn make_checker(config: Config) -> (impl Fn() -> bool, String) {
    // Bind the field to a local, then move only that local into the closure.
    let threshold = config.threshold;
    let checker = move || threshold > 0; // moves `threshold` (i32, Copy), not `config`

    // `config.label` is still available here.
    (checker, config.label)
}

fn demo_bind_first() {
    let cfg = Config { threshold: 5, label: String::from("info") };
    let (check, label) = make_checker(cfg);
    println!("label returned: {label}");
    assert!(check());
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
- own-borrow-over-clone
