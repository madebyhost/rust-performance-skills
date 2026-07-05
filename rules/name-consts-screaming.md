# name-consts-screaming

## id
name-consts-screaming

## severity
medium

## trigger
Use `SCREAMING_SNAKE_CASE` for constants and statics. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
// lowercase/camelCase constants - compiler warns
const maxConnections: u32 = 100;  // warning
const default_timeout: u64 = 30;  // warning
static globalCounter: AtomicU64 = AtomicU64::new(0);  // warning
```

## good
```rust
// SCREAMING_SNAKE_CASE for constants
const MAX_CONNECTIONS: u32 = 100;
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);
const BUFFER_SIZE: usize = 4096;

// SCREAMING_SNAKE_CASE for statics
static GLOBAL_COUNTER: AtomicU64 = AtomicU64::new(0);
static CONFIG: OnceLock<Config> = OnceLock::new();

// Type-level constants in impl blocks
impl Buffer {
    const INITIAL_CAPACITY: usize = 1024;
    const MAX_CAPACITY: usize = 1024 * 1024;
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
- name-funcs-snake
- name-types-camel
- type-newtype-ids
