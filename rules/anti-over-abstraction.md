# anti-over-abstraction

## id
anti-over-abstraction

## severity
reference

## trigger
Don't over-abstract with excessive generics. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Overly generic for a simple function
fn add<T, U, R>(a: T, b: U) -> R
where
    T: Into<R>,
    U: Into<R>,
    R: std::ops::Add<Output = R>,
{
    a.into() + b.into()
}

// Just call add(1, 2) - why make it this complex?

// Trait explosion
trait Readable {}
trait Writable {}
trait ReadWritable: Readable + Writable {}
trait AsyncReadable {}
trait AsyncWritable {}
trait AsyncReadWritable: AsyncReadable + AsyncWritable {}

// Abstract factory pattern (Java flashback)
trait Factory<T> {
    fn create(&self) -> T;
}
trait FactoryFactory<F: Factory<T>, T> {
    fn create_factory(&self) -> F;
}
```

## good
```rust
// Concrete implementation - clear and simple
fn add_i32(a: i32, b: i32) -> i32 {
    a + b
}

// Generic when actually needed (e.g., library code)
fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {
    a + b
}

// Simple traits for actual polymorphism needs
trait Storage {
    fn save(&self, key: &str, value: &[u8]) -> Result<(), Error>;
    fn load(&self, key: &str) -> Result<Vec<u8>, Error>;
}

// Concrete types first
struct FileStorage { path: PathBuf }
struct MemoryStorage { data: HashMap<String, Vec<u8>> }
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
- anti-type-erasure
- api-sealed-trait
- type-generic-bounds
