# api-impl-into

## id
api-impl-into

## severity
high

## trigger
Accept `impl Into<T>` for flexible APIs, implement `From<T>` for conversions. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Requires exact type - forces callers to convert
fn process_path(path: PathBuf) { ... }
fn set_name(name: String) { ... }

// Caller must convert explicitly
process_path(PathBuf::from("/path/to/file"));
process_path("/path/to/file".to_path_buf());  // Verbose
process_path("/path/to/file".into());          // Explicit

set_name(String::from("Alice"));
set_name("Alice".to_string());  // Verbose
```

## good
```rust
// Accept anything that converts to the target type
fn process_path(path: impl Into<PathBuf>) {
    let path = path.into();  // Convert once inside
    // ...
}

fn set_name(name: impl Into<String>) {
    let name = name.into();
    // ...
}

// Callers are ergonomic
process_path("/path/to/file");    // &str converts automatically
process_path(PathBuf::from(".")); // PathBuf works too

set_name("Alice");                // &str
set_name(String::from("Alice"));  // String
set_name(format!("User-{}", id)); // String from format!
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
- api-from-not-into
- api-impl-asref
- err-from-impl
