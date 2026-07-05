# name-lifetime-short

## id
name-lifetime-short

## severity
medium

## trigger
Use short, conventional lifetime names: `'a`, `'b`, `'de`, `'src`. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
// Overly verbose lifetimes
fn parse<'input_lifetime, 'output_lifetime>(
    input: &'input_lifetime str
) -> Result<&'output_lifetime str, Error> { ... }

// Meaningless long names
struct Parser<'parser_instance_lifetime> {
    source: &'parser_instance_lifetime str,
}
```

## good
```rust
// Standard short lifetimes
fn parse<'a>(input: &'a str) -> Result<&'a str, Error> { ... }

struct Parser<'a> {
    source: &'a str,
}

// Multiple lifetimes: 'a, 'b, 'c
fn merge<'a, 'b>(first: &'a str, second: &'b str) -> String { ... }

// Descriptive when clarity helps
fn deserialize<'de>(input: &'de [u8]) -> Result<Value<'de>, Error> { ... }
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
- name-type-param-single
- own-borrow-over-clone
- own-lifetime-elision
