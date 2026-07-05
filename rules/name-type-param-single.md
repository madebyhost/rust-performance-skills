# name-type-param-single

## id
name-type-param-single

## severity
medium

## trigger
Use single uppercase letters for type parameters: `T`, `E`, `K`, `V`. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
// Verbose type parameters
struct Container<ElementType> {
    items: Vec<ElementType>,
}

fn process<InputType, OutputType>(input: InputType) -> OutputType { ... }

// Lowercase - looks like lifetime
struct Wrapper<t> { ... }  // Confusing
```

## good
```rust
// Single uppercase letters
struct Container<T> {
    items: Vec<T>,
}

fn process<I, O>(input: I) -> O { ... }

// Standard conventions
struct HashMap<K, V> { ... }     // K=Key, V=Value
enum Result<T, E> { ... }         // T=Type, E=Error
enum Option<T> { ... }            // T=Type
struct Ref<'a, T> { ... }        // Lifetime + Type
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
- name-lifetime-short
- name-types-camel
- type-generic-bounds
