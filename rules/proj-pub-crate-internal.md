# proj-pub-crate-internal

## id
proj-pub-crate-internal

## severity
low

## trigger
Use pub(crate) for internal APIs. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```rust
// Everything public - users depend on internals
pub mod internal {
    pub struct InternalState {
        pub buffer: Vec<u8>,    // Implementation detail exposed
        pub dirty: bool,
    }

    pub fn process_internal(state: &mut InternalState) {
        // Users can call this, creating coupling
    }
}

pub struct Widget {
    pub state: internal::InternalState,  // Exposed!
}
```

## good
```rust
// Internal module with crate visibility
pub(crate) mod internal {
    pub(crate) struct InternalState {
        pub(crate) buffer: Vec<u8>,
        pub(crate) dirty: bool,
    }

    pub(crate) fn process_internal(state: &mut InternalState) {
        // Only callable within crate
    }
}

pub struct Widget {
    state: internal::InternalState,  // Private field
}

impl Widget {
    pub fn new() -> Self {
        Self {
            state: internal::InternalState {
                buffer: Vec::new(),
                dirty: false,
            }
        }
    }

    pub fn do_something(&mut self) {
        internal::process_internal(&mut self.state);
    }
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
- api-non-exhaustive
- proj-pub-super-parent
- proj-pub-use-reexport
