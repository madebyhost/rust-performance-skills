# doc-module-inner

## id
doc-module-inner

## severity
medium

## trigger
Use `//!` for module-level documentation. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
// This module handles authentication
// It provides JWT and session-based auth

mod auth;

pub use auth::*;
```

```rust
// auth.rs
/// Authentication utilities  // Wrong: this documents nothing useful
use std::collections::HashMap;

pub struct Session { /* ... */ }
```

## good
```rust
//! Authentication and authorization utilities.
//!
//! This module provides multiple authentication strategies:
//!
//! - [`JwtAuth`] - JSON Web Token based authentication
//! - [`SessionAuth`] - Cookie-based session authentication
//! - [`ApiKeyAuth`] - API key authentication for services
//!
//! # Examples
//!
//! ```
//! use my_crate::auth::{JwtAuth, Authenticator};
//!
//! let auth = JwtAuth::new("secret-key");
//! let token = auth.generate_token(&user)?;
//! ```
//!
//! # Feature Flags
//!
//! - `jwt` - Enables JWT authentication (enabled by default)
//! - `sessions` - Enables session-based authentication

use std::collections::HashMap;

pub struct Session { /* ... */ }
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
- doc-all-public
- doc-cargo-metadata
- doc-examples-section
