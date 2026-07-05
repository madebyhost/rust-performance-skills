# anti-format-hot-path

## id
anti-format-hot-path

## severity
reference

## trigger
Don't use format! in hot paths. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// format! in loop - allocates every iteration
fn log_events(events: &[Event]) {
    for event in events {
        let message = format!("[{}] {}: {}", event.level, event.source, event.message);
        logger.log(&message);
    }
}

// format! for building parts
fn build_url(base: &str, path: &str, params: &[(&str, &str)]) -> String {
    let mut url = format!("{}{}", base, path);
    for (key, value) in params {
        url = format!("{}{}={}&", url, key, value);  // New allocation each time
    }
    url
}

// format! for simple concatenation
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)  // Fine for one-off, bad if called 1M times
}
```

## good
```rust
use std::fmt::Write;

// Reuse buffer across iterations
fn log_events(events: &[Event]) {
    let mut buffer = String::with_capacity(256);
    for event in events {
        buffer.clear();
        write!(buffer, "[{}] {}: {}", event.level, event.source, event.message).unwrap();
        logger.log(&buffer);
    }
}

// Build incrementally in single buffer
fn build_url(base: &str, path: &str, params: &[(&str, &str)]) -> String {
    let mut url = String::with_capacity(base.len() + path.len() + params.len() * 20);
    url.push_str(base);
    url.push_str(path);
    for (key, value) in params {
        write!(url, "{}={}&", key, value).unwrap();
    }
    url
}

// For truly hot paths, avoid allocation entirely
fn greet_to_buf(name: &str, buffer: &mut String) {
    buffer.clear();
    buffer.push_str("Hello, ");
    buffer.push_str(name);
    buffer.push('!');
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
- mem-avoid-format
- mem-reuse-collections
- mem-write-over-format
