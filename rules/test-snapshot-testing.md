# test-snapshot-testing

## id
test-snapshot-testing

## severity
medium

## trigger
Use snapshot testing (insta) for complex or serialized output. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
#[test]
fn test_render_error() {
    let err = AppError::NotFound { id: 42 };
    // Fragile: must manually maintain this string forever
    assert_eq!(
        format!("{err}"),
        "resource with id 42 was not found in the database and could not be retrieved"
    );
}

#[test]
fn test_config_serialization() {
    let config = Config::default();
    let json = serde_json::to_string_pretty(&config).unwrap();
    // Hard to read, hard to update, easy to get wrong
    assert_eq!(json, "{\n  \"timeout\": 30,\n  \"retries\": 3\n}");
}
```

## good
```toml
[dev-dependencies]
insta = { version = "1", features = ["json", "yaml"] }
```

```rust
use insta::assert_debug_snapshot;
use insta::assert_json_snapshot;

#[test]
fn test_render_error() {
    let err = AppError::NotFound { id: 42 };
    // On first run: creates snapshots/test_render_error.snap
    // On subsequent runs: diffs against the saved snapshot
    assert_debug_snapshot!(err);
}

#[test]
fn test_config_serialization() {
    let config = Config::default();
    // Snapshot stored as pretty-printed JSON for easy review
    assert_json_snapshot!(config);
}

#[test]
fn test_cli_output() {
    let output = run_cli(&["--help"]);
    // Named snapshot for clarity
    assert_debug_snapshot!("cli_help_output", output);
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Verify the test fails before the fix and covers the intended behavior rather than implementation detail.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- test-arrange-act-assert
- test-doctest-examples
- test-proptest-properties
