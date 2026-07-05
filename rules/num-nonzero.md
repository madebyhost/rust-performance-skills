# num-nonzero

## id
num-nonzero

## severity
high

## trigger
Use `NonZero*` types to forbid zero and unlock the niche optimization. Trigger when working on numeric safety and the code shows `num`-class risk.

## bad
```rust
// caller must remember never to pass 0, but nothing enforces it
fn divide(numerator: u32, denominator: u32) -> u32 {
    assert!(denominator != 0, "denominator must not be zero");
    numerator / denominator
}

// ID of 0 is "invalid" by convention - not enforced
struct Widget {
    id: u32,  // 0 means "not yet assigned" - stringly-typed convention
}
```

## good
```rust
use std::num::NonZeroU32;
use std::mem::size_of;

// zero is rejected at construction; division is always safe
fn divide(numerator: u32, denominator: NonZeroU32) -> u32 {
    numerator / denominator.get()
}

// ID is guaranteed non-zero; Option<WidgetId> is free
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct WidgetId(NonZeroU32);

impl WidgetId {
    /// Returns `None` if `id` is zero.
    pub fn new(id: u32) -> Option<Self> {
        NonZeroU32::new(id).map(WidgetId)
    }

    pub fn get(self) -> u32 {
        self.0.get()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::num::NonZeroU32;

    #[test]
    fn nonzero_new_returns_none_for_zero() {
        assert!(NonZeroU32::new(0).is_none());
        assert!(NonZeroU32::new(1).is_some());
    }

    #[test]
    fn option_nonzero_is_same_size_as_u32() {
        // niche optimization: no space overhead for Option
        assert_eq!(size_of::<Option<NonZeroU32>>(), size_of::<u32>());
        assert_eq!(size_of::<Option<NonZeroU32>>(), 4);
    }

    #[test]
    fn widget_id_rejects_zero() {
        assert!(WidgetId::new(0).is_none());
        let id = WidgetId::new(42).unwrap();
        assert_eq!(id.get(), 42);
    }

    #[test]
    fn divide_uses_nonzero_denominator() {
        let denom = NonZeroU32::new(3).unwrap();
        assert_eq!(divide(12, denom), 4);
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
- mem-smaller-integers
- type-newtype-ids
