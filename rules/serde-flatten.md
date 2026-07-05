# serde-flatten

## id
serde-flatten

## severity
medium

## trigger
Inline nested structs or capture extra keys with `#[serde(flatten)]`. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};

// Duplicated pagination fields in every list response
#[derive(Serialize, Deserialize, Debug)]
struct UserListResponse {
    users: Vec<String>,
    page: u32,
    per_page: u32,
    total: u64,
}

#[derive(Serialize, Deserialize, Debug)]
struct PostListResponse {
    posts: Vec<String>,
    page: u32,       // copy-paste
    per_page: u32,   // copy-paste
    total: u64,      // copy-paste
}
```

## good
```rust
use serde::{Serialize, Deserialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug)]
struct Pagination {
    page: u32,
    per_page: u32,
    total: u64,
}

#[derive(Serialize, Deserialize, Debug)]
struct UserListResponse {
    users: Vec<String>,
    #[serde(flatten)]
    pagination: Pagination,
}

#[derive(Serialize, Deserialize, Debug)]
struct PostListResponse {
    posts: Vec<String>,
    #[serde(flatten)]
    pagination: Pagination,
}

// Capture unknown/dynamic keys into a map
#[derive(Serialize, Deserialize, Debug)]
struct FlexibleConfig {
    name: String,
    version: u32,
    #[serde(flatten)]
    extra: HashMap<String, serde_json::Value>,
}
```

`UserListResponse` serializes to `{"users":[...],"page":1,"per_page":20,"total":100}` - the `Pagination` fields appear at the top level, not nested under a `"pagination"` key.

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not make serde strict when extension fields are expected or when backward compatibility requires tolerance.

## verification
Use golden fixtures, versioned payload tests, and compatibility checks for unknown or missing fields.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- serde-deny-unknown-fields
- serde-enum-representation
