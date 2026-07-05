# doc-hidden-setup

## id
doc-hidden-setup

## severity
medium

## trigger
Use `# ` prefix to hide example setup code. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Processes a batch of items.
///
/// # Examples
///
/// ```
/// use my_crate::{Processor, Config, Item};
/// use std::sync::Arc;
///
/// let config = Config {
///     batch_size: 100,
///     timeout_ms: 5000,
///     retry_count: 3,
/// };
/// let processor = Processor::new(Arc::new(config));
/// let items = vec![
///     Item::new("a"),
///     Item::new("b"),
///     Item::new("c"),
/// ];
///
/// // This is the actual example - buried after 15 lines of setup
/// let results = processor.process_batch(&items)?;
/// assert!(results.all_succeeded());
/// # Ok::<(), my_crate::Error>(())
/// ```
pub fn process_batch(&self, items: &[Item]) -> Result<Results, Error> {
    // ...
}
```

## good
```rust
/// Processes a batch of items.
///
/// # Examples
///
/// ```
/// # use my_crate::{Processor, Config, Item, Error};
/// # use std::sync::Arc;
/// # let config = Config { batch_size: 100, timeout_ms: 5000, retry_count: 3 };
/// # let processor = Processor::new(Arc::new(config));
/// # let items = vec![Item::new("a"), Item::new("b"), Item::new("c")];
/// let results = processor.process_batch(&items)?;
/// assert!(results.all_succeeded());
/// # Ok::<(), Error>(())
/// ```
pub fn process_batch(&self, items: &[Item]) -> Result<Results, Error> {
    // ...
}
```

Users see only:

```rust
let results = processor.process_batch(&items)?;
assert!(results.all_succeeded());
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
- doc-examples-section
- doc-question-mark
- test-doctest-examples
