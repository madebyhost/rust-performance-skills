# trait-coherence-newtype

## id
trait-coherence-newtype

## severity
medium

## trigger
Respect the orphan rule; wrap a foreign type in a newtype to implement a foreign trait on it. Trigger when working on traits and generics and the code shows `trait`-class risk.

## bad
```rust
use std::fmt;

// error[E0117]: only traits defined in the current crate can be implemented for
// types defined outside of the crate
// impl fmt::Display for Vec<i32> { ... }  // both `Display` and `Vec` are foreign
```

## good
```rust
use std::fmt;

// A local newtype wrapping the foreign type.
// `#[repr(transparent)]` guarantees the same memory layout as Vec<i32>.
#[repr(transparent)]
struct CommaSeparated(Vec<i32>);

impl CommaSeparated {
    pub fn new(v: Vec<i32>) -> Self { Self(v) }

    // Provide access to the inner value.
    pub fn into_inner(self) -> Vec<i32> { self.0 }
    pub fn inner(&self) -> &Vec<i32> { &self.0 }
}

// Now both the trait (Display) is foreign and the type (CommaSeparated) is local -
// the orphan rule is satisfied because CommaSeparated is defined here.
impl fmt::Display for CommaSeparated {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut iter = self.0.iter().peekable();
        while let Some(n) = iter.next() {
            write!(f, "{n}")?;
            if iter.peek().is_some() {
                write!(f, ", ")?;
            }
        }
        Ok(())
    }
}

// Implement From/Into so conversion is ergonomic.
impl From<Vec<i32>> for CommaSeparated {
    fn from(v: Vec<i32>) -> Self { Self(v) }
}

impl From<CommaSeparated> for Vec<i32> {
    fn from(w: CommaSeparated) -> Self { w.0 }
}

fn demo() {
    let nums = CommaSeparated::new(vec![1, 2, 3, 4, 5]);
    println!("{nums}");   // "1, 2, 3, 4, 5"

    // Round-trip through the inner type.
    let v: Vec<i32> = nums.into();
    let again = CommaSeparated::from(v);
    println!("{again}");
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
- api-from-not-into
- api-newtype-safety
- trait-blanket-impl
- type-repr-transparent
