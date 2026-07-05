# name-types-camel

## id
name-types-camel

## severity
medium

## trigger
Use `UpperCamelCase` for types, traits, and enum names. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
// Lowercase types - compiler warns
struct http_client { ... }  // warning: type `http_client` should have an upper camel case name
trait serializable { ... }  // warning
enum response_type { ... }  // warning

// Screaming case for types
struct HTTP_CLIENT { ... }  // Not idiomatic
```

## good
```rust
// UpperCamelCase for all types
struct HttpClient { ... }
trait Serializable { ... }
enum ResponseType { ... }

// Compound words
struct TcpConnection { ... }
struct IoError { ... }
struct FileReader { ... }

// Generic types
struct HashMap<K, V> { ... }
struct Result<T, E> { ... }
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
- name-acronym-word
- name-funcs-snake
- name-variants-camel
