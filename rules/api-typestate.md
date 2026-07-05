# api-typestate

## id
api-typestate

## severity
high

## trigger
Use typestate pattern to encode state machine invariants in the type system. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
struct Connection {
    state: ConnectionState,
    socket: Option<TcpStream>,
}

enum ConnectionState {
    Disconnected,
    Connected,
    Authenticated,
}

impl Connection {
    fn send(&mut self, data: &[u8]) -> Result<(), Error> {
        // Runtime check - can fail if called in wrong state
        if self.state != ConnectionState::Authenticated {
            return Err(Error::NotAuthenticated);
        }
        self.socket.as_mut().unwrap().write_all(data)?;
        Ok(())
    }

    fn authenticate(&mut self, password: &str) -> Result<(), Error> {
        // Runtime check - can fail
        if self.state != ConnectionState::Connected {
            return Err(Error::NotConnected);
        }
        // ...
    }
}

// Bug: forgot to authenticate
let mut conn = Connection::new();
conn.connect()?;
conn.send(b"data")?;  // Runtime error: NotAuthenticated
```

## good
```rust
// Different types for each state
struct Disconnected;
struct Connected { socket: TcpStream }
struct Authenticated { socket: TcpStream, session: Session }

struct Connection<State> {
    state: State,
}

impl Connection<Disconnected> {
    fn new() -> Self {
        Connection { state: Disconnected }
    }

    fn connect(self, addr: &str) -> Result<Connection<Connected>, Error> {
        let socket = TcpStream::connect(addr)?;
        Ok(Connection { state: Connected { socket } })
    }
}

impl Connection<Connected> {
    fn authenticate(self, password: &str) -> Result<Connection<Authenticated>, Error> {
        let session = do_auth(&self.state.socket, password)?;
        Ok(Connection {
            state: Authenticated { socket: self.state.socket, session }
        })
    }
}

impl Connection<Authenticated> {
    fn send(&mut self, data: &[u8]) -> Result<(), Error> {
        // No runtime check needed - type guarantees we're authenticated
        self.state.socket.write_all(data)?;
        Ok(())
    }
}

// Bug: forgot to authenticate
let conn = Connection::new();
let conn = conn.connect("server:8080")?;
conn.send(b"data");  // Compile error! send() not available on Connection<Connected>

// Correct usage
let conn = Connection::new();
let conn = conn.connect("server:8080")?;
let mut conn = conn.authenticate("secret")?;
conn.send(b"data")?;  // Works - type is Connection<Authenticated>
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
- api-builder-pattern
- api-parse-dont-validate
- api-sealed-trait
