# name-iter-method

## id
name-iter-method

## severity
medium

## trigger
Name iterator methods `iter()`, `iter_mut()`, and `into_iter()` consistently. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
struct Collection<T> {
    items: Vec<T>,
}

impl<T> Collection<T> {
    // Non-standard names - confusing
    fn elements(&self) -> impl Iterator<Item = &T> {
        self.items.iter()
    }

    fn get_iterator(&self) -> impl Iterator<Item = &T> {
        self.items.iter()
    }

    fn to_iter(self) -> impl Iterator<Item = T> {
        self.items.into_iter()
    }
}
```

## good
```rust
struct Collection<T> {
    items: Vec<T>,
}

impl<T> Collection<T> {
    /// Returns an iterator over references.
    fn iter(&self) -> impl Iterator<Item = &T> {
        self.items.iter()
    }

    /// Returns an iterator over mutable references.
    fn iter_mut(&mut self) -> impl Iterator<Item = &mut T> {
        self.items.iter_mut()
    }
}

// Implement IntoIterator for for-loop support
impl<T> IntoIterator for Collection<T> {
    type Item = T;
    type IntoIter = std::vec::IntoIter<T>;

    fn into_iter(self) -> Self::IntoIter {
        self.items.into_iter()
    }
}

impl<'a, T> IntoIterator for &'a Collection<T> {
    type Item = &'a T;
    type IntoIter = std::slice::Iter<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        self.items.iter()
    }
}

impl<'a, T> IntoIterator for &'a mut Collection<T> {
    type Item = &'a mut T;
    type IntoIter = std::slice::IterMut<'a, T>;

    fn into_iter(self) -> Self::IntoIter {
        self.items.iter_mut()
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
- api-common-traits
- api-extension-trait
- name-as-free
