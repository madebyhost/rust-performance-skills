# serde-enum-representation

## id
serde-enum-representation

## severity
medium

## trigger
Choose enum tagging deliberately: externally, internally, adjacently tagged, or untagged. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};

// Default: externally tagged. Serializes as {"Circle":{"radius":5.0}}
// Most REST APIs expect {"type":"circle","radius":5.0} instead.
#[derive(Serialize, Deserialize, Debug)]
enum Shape {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}
```

## good
```rust
use serde::{Serialize, Deserialize};

// Externally tagged (default) - {"Circle":{"radius":5.0}}
// Good for: Rust-to-Rust, when the variant name IS the key
#[derive(Serialize, Deserialize, Debug)]
enum ShapeExternal {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}

// Internally tagged - {"type":"Circle","radius":5.0}
// Good for: REST APIs with a discriminator field; all variants must be structs/maps
#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "type")]
enum ShapeInternal {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}

// Adjacently tagged - {"t":"Circle","c":{"radius":5.0}}
// Good for: when variants may contain primitives or vecs (internally tagged can't handle those)
#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "t", content = "c")]
enum ShapeAdjacent {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
    Count(u32),  // tuple variant - works here, but NOT with internally tagged
}

// Untagged - {"radius":5.0}
// Good for: wrapping a small number of clearly distinct types; avoid otherwise
#[derive(Serialize, Deserialize, Debug)]
#[serde(untagged)]
enum Value {
    Integer(i64),
    Float(f64),
    Text(String),
}
```

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
- api-non-exhaustive
- serde-flatten
- type-enum-states
