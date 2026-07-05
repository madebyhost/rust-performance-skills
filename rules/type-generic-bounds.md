# type-generic-bounds

## id
type-generic-bounds

## severity
medium

## trigger
Add trait bounds only where needed, prefer where clauses for readability. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
// Bounds on struct definition - limits all uses
struct Container<T: Clone + Debug> {  // Even storage requires Clone?
    items: Vec<T>,
}

// Inline bounds make signature hard to read
fn process<T: Clone + Debug + Send + Sync + 'static, E: Error + Send + Clone>(
    value: T
) -> Result<T, E> { ... }

// Redundant bounds
fn print_twice<T: Clone + Debug>(value: T)
where
    T: Clone,  // Already specified above
{ ... }
```

## good
```rust
// No bounds on struct - store anything
struct Container<T> {
    items: Vec<T>,
}

// Bounds only on impls that need them
impl<T: Clone> Container<T> {
    fn duplicate(&self) -> Self {
        Container { items: self.items.clone() }
    }
}

impl<T: Debug> Container<T> {
    fn debug_print(&self) {
        println!("{:?}", self.items);
    }
}

// Where clause for readability
fn process<T, E>(value: T) -> Result<T, E>
where
    T: Clone + Debug + Send + Sync + 'static,
    E: Error + Send + Clone,
{ ... }
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not encode every boolean as typestate; use the type system when it removes real invalid states.

## verification
Add constructor tests, compile-fail tests where useful, and property tests for invariants.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-impl-asref
- api-impl-into
- name-type-param-single
- trait-associated-type-vs-generic
- trait-dyn-vs-generic
