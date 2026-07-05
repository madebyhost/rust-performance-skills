# type-enum-states

## id
type-enum-states

## severity
medium

## trigger
Use enums for mutually exclusive states. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
struct Connection {
    is_connected: bool,
    is_authenticated: bool,
    is_disconnected: bool,  // Can all three be true? False?
    socket: Option<TcpStream>,
    credentials: Option<Credentials>,
}

// Possible invalid states:
// - is_connected && is_disconnected (contradiction)
// - is_authenticated && !is_connected (impossible)
// - socket is None but is_connected is true (inconsistent)
```

## good
```rust
enum ConnectionState {
    Disconnected,
    Connecting { address: SocketAddr },
    Connected { socket: TcpStream },
    Authenticated { socket: TcpStream, session: Session },
    Failed { error: ConnectionError },
}

struct Connection {
    state: ConnectionState,
}

// Impossible states are unrepresentable
// Each state has exactly the data it needs
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not encode every boolean as typestate; use the type system when it removes real invalid states.

## verification
Add constructor tests, compile-fail tests where useful, and property tests for invariants.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-non-exhaustive
- api-typestate
- pat-exhaustive-enum
- serde-enum-representation
- type-option-nullable
