# obs-library-facade

## id
obs-library-facade

## severity
medium

## trigger
Libraries emit through the tracing/log facade and never install a subscriber. Trigger when working on observability and the code shows `obs`-class risk.

## bad
```rust
// In a library crate: mylib/src/lib.rs
use tracing::info;

pub fn connect(url: &str) {
    // BAD: library installs a subscriber - conflicts with the application
    tracing_subscriber::fmt::init();
    info!(url, "connecting");
}
```

```rust
// Also bad: using env_logger in a library
pub fn init_logging() {
    env_logger::init(); // steals the global logger from the application
}
```

## good
```rust
// In a library crate: mylib/src/lib.rs
use tracing::info;

pub fn connect(url: &str) {
    // Good: just emit; the application owns subscriber setup
    info!(url, "connecting");
}
```

```rust
// In the binary: src/main.rs
fn main() {
    // The application initializes once, with full control
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    mylib::connect("postgres://localhost/app");
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
- api-serde-optional
- obs-levels-filter
- obs-tracing-over-log
