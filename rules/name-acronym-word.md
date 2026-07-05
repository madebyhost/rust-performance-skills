# name-acronym-word

## id
name-acronym-word

## severity
medium

## trigger
Treat acronyms as words in identifiers: `HttpServer`, not `HTTPServer`. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
// ALL CAPS acronyms - unclear word boundaries
struct HTTPServer { ... }      // HTTP + Server or H + TTP + Server?
struct TCPIPConnection { ... } // TCP + IP? Or other splits?
struct JSONParser { ... }
struct XMLHTTPRequest { ... }  // Very confusing

fn parseJSON(input: &str) { ... }
fn connectTCP(addr: &str) { ... }
```

## good
```rust
// Acronyms as words - clear boundaries
struct HttpServer { ... }      // Http + Server
struct TcpIpConnection { ... } // Tcp + Ip + Connection
struct JsonParser { ... }
struct XmlHttpRequest { ... }

fn parse_json(input: &str) { ... }
fn connect_tcp(addr: &str) { ... }

// More examples
struct Uuid { ... }            // Not UUID
struct Uri { ... }             // Not URI
struct Url { ... }             // Not URL
struct Html { ... }            // Not HTML
struct Css { ... }             // Not CSS
struct Api { ... }             // Not API
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
- name-consts-screaming
- name-funcs-snake
- name-types-camel
