# type-newtype-ids

## id
type-newtype-ids

## severity
medium

## trigger
Wrap IDs in newtypes: `UserId(u64)`. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
fn get_user_posts(user_id: u64, post_id: u64) -> Vec<Post> {
    // Which is which? Easy to swap by accident
}

// Oops! Arguments swapped - compiles fine, wrong at runtime
let posts = get_user_posts(post_id, user_id);

// Even worse with multiple IDs
fn transfer(from: u64, to: u64, amount: u64) {
    // from/to can easily be swapped
}
```

## good
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(pub u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct PostId(pub u64);

fn get_user_posts(user_id: UserId, post_id: PostId) -> Vec<Post> {
    // Types are distinct
}

// This won't compile - types don't match
// let posts = get_user_posts(post_id, user_id);  // ERROR!

// Correct usage
let posts = get_user_posts(UserId(1), PostId(42));
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
- api-parse-dont-validate
- num-nonzero
- type-newtype-validated
