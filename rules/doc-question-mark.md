# doc-question-mark

## id
doc-question-mark

## severity
medium

## trigger
Use `?` in examples, not `.unwrap()`. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Reads a configuration file.
///
/// # Examples
///
/// ```
/// let config = Config::from_file("config.toml").unwrap();
/// println!("{:?}", config.database_url);
/// ```
pub fn from_file(path: &str) -> Result<Config, Error> {
    // ...
}

/// Fetches data from the API.
///
/// # Examples
///
/// ```
/// let client = Client::new();
/// let response = client.get("https://api.example.com").unwrap();
/// let data: Data = response.json().unwrap();
/// ```
pub async fn get(&self, url: &str) -> Result<Response, Error> {
    // ...
}
```

## good
```rust
/// Reads a configuration file.
///
/// # Examples
///
/// ```
/// # use my_crate::{Config, Error};
/// # fn main() -> Result<(), Error> {
/// let config = Config::from_file("config.toml")?;
/// println!("{:?}", config.database_url);
/// # Ok(())
/// # }
/// ```
pub fn from_file(path: &str) -> Result<Config, Error> {
    // ...
}

/// Fetches data from the API.
///
/// # Examples
///
/// ```no_run
/// # use my_crate::{Client, Data, Error};
/// # async fn example() -> Result<(), Error> {
/// let client = Client::new();
/// let response = client.get("https://api.example.com").await?;
/// let data: Data = response.json().await?;
/// # Ok(())
/// # }
/// ```
pub async fn get(&self, url: &str) -> Result<Response, Error> {
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
- doc-examples-section
- doc-hidden-setup
- err-question-mark
