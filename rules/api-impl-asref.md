# api-impl-asref

## id
api-impl-asref

## severity
high

## trigger
Use `AsRef<T>` when you only need to borrow the inner data. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Forces callers to provide exact types
fn process_text(text: &str) { ... }
fn read_file(path: &Path) { ... }

// Can't call directly with owned types
let s = String::from("hello");
process_text(&s);  // Works but verbose

let p = PathBuf::from("/file");
read_file(&p);  // Works but verbose
read_file("/file");  // Error! &str != &Path
```

## good
```rust
// Accept anything that can be viewed as the target type
fn process_text(text: impl AsRef<str>) {
    let s: &str = text.as_ref();
    println!("{}", s);
}

fn read_file(path: impl AsRef<Path>) -> io::Result<Vec<u8>> {
    std::fs::read(path.as_ref())
}

// All of these work:
process_text("literal");        // &str
process_text(String::from("owned"));  // String
process_text(Cow::from("cow")); // Cow<str>

read_file("/path/to/file");     // &str
read_file(Path::new("/path"));  // &Path
read_file(PathBuf::from("/path")); // PathBuf
read_file(OsStr::new("/path")); // &OsStr
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
- api-impl-into
- own-borrow-over-clone
- own-slice-over-vec
