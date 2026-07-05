# trait-default-methods

## id
trait-default-methods

## severity
medium

## trigger
Define a trait in terms of a few required methods plus defaulted ones built on top of them. Trigger when working on traits and generics and the code shows `trait`-class risk.

## bad
```rust
// Every implementor must manually implement all three methods,
// even though two of them are mechanical compositions of the first.
trait Summarise {
    fn sentences(&self) -> Vec<String>;
    fn first_sentence(&self) -> Option<String>;  // always just sentences().into_iter().next()
    fn word_count(&self) -> usize;               // always sentences().join(" ").split_whitespace().count()
}

struct Article { body: String }

impl Summarise for Article {
    fn sentences(&self) -> Vec<String> {
        self.body.split('.').map(str::trim).map(str::to_owned).collect()
    }
    // Duplicated logic - must be kept in sync across every implementor.
    fn first_sentence(&self) -> Option<String> {
        self.sentences().into_iter().next()
    }
    fn word_count(&self) -> usize {
        self.sentences().join(" ").split_whitespace().count()
    }
}
```

## good
```rust
trait Summarise {
    // ----- Required: the only thing implementors must provide -----
    fn sentences(&self) -> Vec<String>;

    // ----- Defaulted: free for all implementors -----
    fn first_sentence(&self) -> Option<String> {
        self.sentences().into_iter().next()
    }

    fn word_count(&self) -> usize {
        self.sentences().join(" ").split_whitespace().count()
    }

    fn is_empty(&self) -> bool {
        self.sentences().is_empty()
    }
}

// Minimal impl - one method, three come for free.
struct Article { body: String }

impl Summarise for Article {
    fn sentences(&self) -> Vec<String> {
        self.body
            .split('.')
            .map(str::trim)
            .filter(|s| !s.is_empty())
            .map(str::to_owned)
            .collect()
    }
}

// Override a default for performance when the default is provably slower.
struct PreSplit { parts: Vec<String> }

impl Summarise for PreSplit {
    fn sentences(&self) -> Vec<String> {
        self.parts.clone()
    }

    // Override: the parts are already split - no need to join and re-split.
    fn word_count(&self) -> usize {
        self.parts.iter().flat_map(|s| s.split_whitespace()).count()
    }
}

fn print_summary(item: &impl Summarise) {
    if item.is_empty() {
        println!("(empty)");
        return;
    }
    if let Some(first) = item.first_sentence() {
        println!("first: {first}");
    }
    println!("words: {}", item.word_count());
}

fn demo() {
    let a = Article { body: "Rust is fast. Rust is safe. Rust is fun.".to_owned() };
    print_summary(&a);

    let p = PreSplit { parts: vec!["hello world".to_owned(), "foo bar baz".to_owned()] };
    print_summary(&p);
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
- api-extension-trait
- trait-associated-type-vs-generic
- trait-blanket-impl
