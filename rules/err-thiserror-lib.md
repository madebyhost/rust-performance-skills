# err-thiserror-lib

## id
err-thiserror-lib

## severity
critical

## trigger
Use `thiserror` for library error types. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
// String errors - not matchable
fn parse(input: &str) -> Result<Data, String> {
    Err("parse error".to_string())
}

// Box<dyn Error> - not matchable
fn load(path: &Path) -> Result<Data, Box<dyn std::error::Error>> {
    Err(Box::new(std::io::Error::new(std::io::ErrorKind::NotFound, "file not found")))
}

// Manual implementation - verbose
#[derive(Debug)]
enum MyError {
    Io(std::io::Error),
    Parse(String),
}

impl std::fmt::Display for MyError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MyError::Io(e) => write!(f, "io error: {}", e),
            MyError::Parse(s) => write!(f, "parse error: {}", s),
        }
    }
}

impl std::error::Error for MyError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            MyError::Io(e) => Some(e),
            MyError::Parse(_) => None,
        }
    }
}
```

## good
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("invalid syntax at line {line}: {message}")]
    Syntax { line: usize, message: String },

    #[error("unexpected end of file")]
    UnexpectedEof,

    #[error("invalid utf-8 encoding")]
    Utf8(#[from] std::str::Utf8Error),

    #[error("io error reading input")]
    Io(#[from] std::io::Error),
}

// Usage
fn parse(input: &str) -> Result<Ast, ParseError> {
    if input.is_empty() {
        return Err(ParseError::UnexpectedEof);
    }
    // ...
}

// Users can match specific errors
match parse(input) {
    Ok(ast) => process(ast),
    Err(ParseError::Syntax { line, message }) => {
        eprintln!("Syntax error on line {}: {}", line, message);
    }
    Err(ParseError::UnexpectedEof) => {
        eprintln!("File ended unexpectedly");
    }
    Err(e) => eprintln!("Error: {}", e),
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
- err-anyhow-app
- err-from-impl
- err-source-chain
