# api-sealed-trait

## id
api-sealed-trait

## severity
high

## trigger
Use sealed traits to prevent external implementations while allowing use. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Anyone can implement this trait
pub trait DatabaseDriver {
    fn connect(&self, url: &str) -> Connection;
    fn execute(&self, query: &str) -> Result<Rows, Error>;
}

// External crate implements it incorrectly
impl DatabaseDriver for MyBadDriver {
    fn connect(&self, url: &str) -> Connection {
        // Buggy implementation that doesn't handle errors
        unsafe { force_connect(url) }
    }
}

// Later, you want to add a required method - BREAKING CHANGE
pub trait DatabaseDriver {
    fn connect(&self, url: &str) -> Connection;
    fn execute(&self, query: &str) -> Result<Rows, Error>;
    fn transaction(&self) -> Transaction;  // External impls now broken!
}
```

## good
```rust
// Create a private module with a private trait
mod private {
    pub trait Sealed {}
}

// Public trait requires the private trait
pub trait DatabaseDriver: private::Sealed {
    fn connect(&self, url: &str) -> Connection;
    fn execute(&self, query: &str) -> Result<Rows, Error>;
}

// Only your crate can implement Sealed, thus DatabaseDriver
pub struct PostgresDriver;
impl private::Sealed for PostgresDriver {}
impl DatabaseDriver for PostgresDriver {
    fn connect(&self, url: &str) -> Connection { ... }
    fn execute(&self, query: &str) -> Result<Rows, Error> { ... }
}

pub struct MySqlDriver;
impl private::Sealed for MySqlDriver {}
impl DatabaseDriver for MySqlDriver {
    fn connect(&self, url: &str) -> Connection { ... }
    fn execute(&self, query: &str) -> Result<Rows, Error> { ... }
}

// External crate cannot implement - private::Sealed is not accessible
// impl DatabaseDriver for ExternalDriver { }  // Error!

// But external code CAN use the trait
fn use_driver(driver: &impl DatabaseDriver) {
    let conn = driver.connect("postgres://localhost");
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not over-generalize a public API before real consumers or compatibility constraints exist.

## verification
Compile examples, run semver checks for public APIs, and add tests for boundary behavior.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-extension-trait
- api-non-exhaustive
- api-typestate
