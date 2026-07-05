# readability-early-return-control-flow

## id
readability-early-return-control-flow

## severity
medium

## trigger
Deeply nested validation, parsing, request handling, or error handling where the happy path is obscured.

## bad
```rust
fn handle(req: Request) -> Result<Response, Error> {
    if req.is_valid() {
        if let Some(user) = req.user {
            if user.active {
                return process(user);
            }
        }
    }
    Err(Error::Invalid)
}
```

## good
```rust
fn handle(req: Request) -> Result<Response, Error> {
    ensure!(req.is_valid(), Error::Invalid);
    let Some(user) = req.user else { return Err(Error::Invalid); };
    ensure!(user.active, Error::Invalid);
    process(user)
}
```

## when
Use when early returns, `let else`, or small extraction makes failure handling explicit and the main path easier to audit.

## when_not
Do not split compact logic into many tiny functions if it hides invariants or makes ownership harder to follow.

## verification
Run tests for every exit path and review whether error context is preserved after flattening.

## sources
- mcpmarket rust-best-practices: https://mcpmarket.com/tools/skills/rust-best-practices
- thrashr888-agent-kit: https://github.com/thrashr888/thrashr888-agent-kit/tree/main/skills/rust-best-practices
- Rust let-else: https://doc.rust-lang.org/rust-by-example/flow_control/let_else.html

## related_rules
- pat-let-else
- err-context-chain
- anti-over-abstraction
