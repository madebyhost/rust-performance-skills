# type-deref-coercion

## id
type-deref-coercion

## severity
medium

## trigger
Implement `Deref`/`DerefMut` only for smart-pointer and transparent wrapper types. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
struct User {
    name: String,
    email: String,
}

struct AdminUser(User);

// Anti-pattern: using Deref to "inherit" User methods on AdminUser
impl std::ops::Deref for AdminUser {
    type Target = User;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// Now AdminUser silently exposes all User fields/methods -
// callers can't tell what AdminUser owns vs. inherits.
fn greet(admin: &AdminUser) {
    println!("hello, {}", admin.name); // surprising implicit deref
}
```

## good
```rust
// Smart-pointer/transparent wrapper: correct use of Deref
struct MyBox<T>(T);

impl<T> std::ops::Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<T> std::ops::DerefMut for MyBox<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

// Domain types: expose only the API you intend, explicitly
struct User {
    pub name: String,
    pub email: String,
}

struct AdminUser(User);

impl AdminUser {
    pub fn name(&self) -> &str {
        &self.0.name
    }

    pub fn email(&self) -> &str {
        &self.0.email
    }

    pub fn can_delete_users(&self) -> bool {
        true
    }
}

fn greet(admin: &AdminUser) {
    println!("hello, {}", admin.name()); // explicit, readable
}
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
- own-borrow-over-clone
- type-newtype-ids
