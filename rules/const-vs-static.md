# const-vs-static

## id
const-vs-static

## severity
medium

## trigger
Use `const` for an inlined value and `static` for a single addressed instance. Trigger when working on compile-time evaluation and the code shows `const`-class risk.

## bad
```rust
// large table as `const` - potentially duplicated at every use site
const LOOKUP: [u8; 256] = [0u8; 256];

// `static mut` - unsafe to read and a hard error in edition 2024
static mut COUNTER: u64 = 0;

// `static` for a tiny value - needlessly takes an address
static TIMEOUT_MS: u64 = 5000;
```

## good
```rust
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{LazyLock, OnceLock};

// small value: `const` - inlined at each use, no address needed
const MAX_RETRIES: u32 = 3;
const TIMEOUT_MS: u64 = 5_000;
const FLAG_MASK: u8 = 0b0000_1111;

// large data: `static` - one copy in the binary, shareable as `&'static`
static LOOKUP: [u8; 256] = [0u8; 256];

fn process(byte: u8) -> u8 {
    LOOKUP[byte as usize]
}

// `&'static str` requires a `static` (or a string literal)
static APP_NAME: &str = "my-app";

// mutable global state - use atomics, not `static mut`
static REQUEST_COUNT: AtomicU64 = AtomicU64::new(0);

fn record_request() {
    REQUEST_COUNT.fetch_add(1, Ordering::Relaxed);
}

// lazily initialized global - `LazyLock` (stable since 1.80)
static CONFIG_PATH: LazyLock<String> = LazyLock::new(|| {
    std::env::var("CONFIG_PATH").unwrap_or_else(|_| "/etc/app/config.toml".to_owned())
});

// single-assignment global - `OnceLock`
static GREETING: OnceLock<String> = OnceLock::new();

fn set_greeting(name: &str) {
    let _ = GREETING.set(format!("hello, {name}"));
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
- name-consts-screaming
- own-mutex-interior
