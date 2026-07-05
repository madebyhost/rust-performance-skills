# proj-pub-super-parent

## id
proj-pub-super-parent

## severity
low

## trigger
Use pub(super) for parent-only visibility. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```rust
// src/parser/mod.rs
pub mod lexer;
pub mod ast;

// src/parser/lexer.rs
pub fn internal_helper() {  // Visible to entire crate!
    // Helper only needed by lexer and ast
}

pub(crate) struct Token {  // Visible to entire crate
    // Only parser submodules need this
}
```

## good
```rust
// src/parser/mod.rs
pub mod lexer;
pub mod ast;

// Shared types for parser submodules only
pub(super) struct Token {
    pub(super) kind: TokenKind,
    pub(super) span: Span,
}

pub(super) fn shared_helper() -> Token {
    // Only visible in parser/*
}

// src/parser/lexer.rs
use super::{Token, shared_helper};

pub fn lex(input: &str) -> Vec<Token> {
    shared_helper();
    // ...
}

// src/parser/ast.rs
use super::Token;

pub fn parse(tokens: Vec<Token>) -> Ast {
    // ...
}
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
- proj-mod-by-feature
- proj-pub-crate-internal
- proj-pub-use-reexport
