# anti-empty-catch

## id
anti-empty-catch

## severity
reference

## trigger
Don't silently ignore errors. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Silently ignores errors
let _ = write_to_file(data);

// Discards error completely
if let Err(_) = send_notification() {
    // Nothing - error vanishes
}

// Converts Result to Option, losing error info
let value = risky_operation().ok();

// Match with empty arm
match database.save(record) {
    Ok(_) => println!("saved"),
    Err(_) => {}  // Silent failure
}

// Ignored in loop
for item in items {
    let _ = process(item);  // Failures unnoticed
}
```

## good
```rust
// Log the error
if let Err(e) = write_to_file(data) {
    error!("failed to write file: {}", e);
}

// Propagate if possible
send_notification()?;

// Or handle explicitly
match send_notification() {
    Ok(_) => info!("notification sent"),
    Err(e) => warn!("notification failed: {}", e),
}

// Collect errors in batch operations
let (successes, failures): (Vec<_>, Vec<_>) = items
    .into_iter()
    .map(process)
    .partition(Result::is_ok);

if !failures.is_empty() {
    warn!("{} items failed to process", failures.len());
}

// Explicit documentation when ignoring
// Intentionally ignored: cleanup failure is not critical
let _ = cleanup_temp_file();  // Add comment explaining why
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
- anti-unwrap-abuse
- err-context-chain
- err-result-over-panic
