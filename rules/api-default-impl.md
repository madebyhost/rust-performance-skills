# api-default-impl

## id
api-default-impl

## severity
high

## trigger
Implement `Default` for types with sensible default values. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
struct Config {
    timeout: Duration,
    retries: u32,
    verbose: bool,
}

impl Config {
    // Custom constructor - works but non-standard
    fn new() -> Self {
        Config {
            timeout: Duration::from_secs(30),
            retries: 3,
            verbose: false,
        }
    }
}

// Can't use with standard patterns
let config: Config = Default::default();  // Error: Default not implemented
let timeout = settings.get("timeout").unwrap_or_default();  // Won't work
```

## good
```rust
use std::time::Duration;

// Simple case: derive uses each field type's Default (Duration::ZERO, 0, false)
#[derive(Default)]
struct Config {
    timeout: Duration,
    retries: u32,
    verbose: bool,
}
```

For a non-zero default, implement `Default` by hand instead of deriving. (Per-field defaults like `timeout: Duration = Duration::from_secs(30)` require the nightly `default_field_values` feature.)

```rust
use std::time::Duration;

struct Config {
    timeout: Duration,
    retries: u32,
    verbose: bool,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            timeout: Duration::from_secs(30),
            retries: 3,
            verbose: false,
        }
    }
}

// Now works with all standard patterns
let config = Config::default();
let config = Config { retries: 5, ..Default::default() };
let value = map.get("key").cloned().unwrap_or_default();
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not over-generalize a public API before real consumers or compatibility constraints exist.

## verification
Compile examples, run semver checks for public APIs, and add tests for boundary behavior.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-builder-pattern
- api-common-traits
- api-from-not-into
