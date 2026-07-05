# type-phantom-marker

## id
type-phantom-marker

## severity
medium

## trigger
Use `PhantomData` to express type relationships without runtime cost. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
// Type parameter unused - compiler error
struct Handle<T> {
    id: u64,
    // Error: parameter `T` is never used
}

// Workaround with unnecessary storage
struct Handle<T> {
    id: u64,
    _type: Option<T>,  // Wastes memory, requires T: Default
}
```

## good
```rust
use std::marker::PhantomData;

struct Handle<T> {
    id: u64,
    _marker: PhantomData<T>,  // Zero-size, tells compiler about T
}

impl<T> Handle<T> {
    fn new(id: u64) -> Self {
        Handle {
            id,
            _marker: PhantomData,
        }
    }
}

// Different Handle types are incompatible
struct User;
struct Order;

fn process_user(h: Handle<User>) { ... }

let user_handle = Handle::<User>::new(1);
let order_handle = Handle::<Order>::new(2);

process_user(user_handle);   // OK
process_user(order_handle);  // Error: expected Handle<User>, found Handle<Order>
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
- api-newtype-safety
- api-typestate
- type-newtype-ids
