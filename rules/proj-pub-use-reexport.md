# proj-pub-use-reexport

## id
proj-pub-use-reexport

## severity
low

## trigger
Use pub use for clean public API. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```rust
// lib.rs - Deep module paths exposed
pub mod error;
pub mod config;
pub mod client;
pub mod types;

// Users must write:
use my_crate::error::MyError;
use my_crate::config::Config;
use my_crate::client::http::HttpClient;
use my_crate::types::request::Request;
```

## good
```rust
// lib.rs - Flat public API
mod error;
mod config;
mod client;
mod types;

pub use error::MyError;
pub use config::Config;
pub use client::http::HttpClient;
pub use types::request::Request;

// Users write:
use my_crate::{Config, HttpClient, MyError, Request};
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
- proj-prelude-module
- proj-pub-crate-internal
