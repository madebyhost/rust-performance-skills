# name-is-has-bool

## id
name-is-has-bool

## severity
medium

## trigger
Use `is_`, `has_`, `can_`, `should_` prefixes for boolean-returning methods. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
impl User {
    // Unclear: does this check or set?
    fn active(&self) -> bool { ... }

    // Unclear: does this delete or check?
    fn deleted(&self) -> bool { ... }

    // Unclear return type
    fn admin(&self) -> bool { ... }
}

// Reading code is confusing
if user.active() { ... }  // Is this checking or activating?
```

## good
```rust
impl User {
    // Clear: answers "is the user active?"
    fn is_active(&self) -> bool { ... }

    // Clear: answers "is the user deleted?"
    fn is_deleted(&self) -> bool { ... }

    // Clear: answers "is the user an admin?"
    fn is_admin(&self) -> bool { ... }

    // Clear: answers "does the user have permission X?"
    fn has_permission(&self, perm: Permission) -> bool { ... }

    // Clear: answers "can the user edit?"
    fn can_edit(&self) -> bool { ... }
}

// Reads naturally
if user.is_active() && user.has_permission(Permission::Write) {
    // ...
}
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
- api-must-use
- name-funcs-snake
- name-no-get-prefix
