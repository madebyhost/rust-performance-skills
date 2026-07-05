# serde-skip-empty

## id
serde-skip-empty

## severity
medium

## trigger
Omit empty fields with `skip_serializing_if`. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct ApiResponse {
    id: u64,
    name: String,
    description: Option<String>,  // serializes as null when None
    tags: Vec<String>,            // serializes as [] when empty
    error: Option<String>,        // serializes as null when None
}
```

Produces: `{"id":1,"name":"Alice","description":null,"tags":[],"error":null}`

## good
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct ApiResponse {
    id: u64,
    name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    description: Option<String>,
    #[serde(skip_serializing_if = "Vec::is_empty")]
    tags: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
    // internal field excluded entirely from the wire format
    #[serde(skip)]
    _cache_key: Option<String>,
}

impl Default for ApiResponse {
    fn default() -> Self {
        ApiResponse {
            id: 0,
            name: String::new(),
            description: None,
            tags: Vec::new(),
            error: None,
            _cache_key: None,
        }
    }
}
```

Produces: `{"id":1,"name":"Alice"}` - absent fields are simply omitted.

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
- serde-default-compat
- serde-rename-all
