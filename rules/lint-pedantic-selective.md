# lint-pedantic-selective

## id
lint-pedantic-selective

## severity
low

## trigger
Enable clippy::pedantic selectively. Trigger when working on linting and the code shows `lint`-class risk.

## bad
```rust
// Too noisy - will fight you constantly
#![warn(clippy::pedantic)]
```

## good
```toml
# Cargo.toml - cherry-pick useful pedantic lints
[lints.clippy]
# Enable pedantic as baseline
pedantic = "warn"

# Disable noisy ones
missing_errors_doc = "allow"      # Document errors separately
missing_panics_doc = "allow"      # Document panics separately
module_name_repetitions = "allow" # Allow Foo::FooError pattern
too_many_lines = "allow"          # Function length varies
must_use_candidate = "allow"      # Too many suggestions
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Run cargo clippy with the intended lint level and document any allow with a narrow reason.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- lint-deny-correctness
- lint-warn-complexity
- lint-warn-style
