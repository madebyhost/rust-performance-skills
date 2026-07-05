# async-cancel-safety

## id
async-cancel-safety

## severity
high

## trigger
Ensure futures used in `tokio::select!` branches are cancellation-safe. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
use tokio::io::{AsyncReadExt, BufReader};
use tokio::net::TcpStream;
use tokio::sync::mpsc;

// Non-cancel-safe: `read_exact` owns an internal buffer inside the future.
// If select! drops this branch, the partially-read bytes are gone.
async fn bad_example(stream: &mut BufReader<TcpStream>, rx: &mut mpsc::Receiver<u8>) {
    let mut buf = [0u8; 1024];
    tokio::select! {
        // BUG: if the `recv` branch fires first, the bytes already read
        // into buf inside `read_exact` are silently discarded
        result = stream.read_exact(&mut buf) => {
            println!("read {} bytes", result.unwrap());
        }
        msg = rx.recv() => {
            println!("got message: {:?}", msg);
        }
    }
}
```

## good
```rust
use tokio::io::{AsyncReadExt, BufReader};
use tokio::net::TcpStream;
use tokio::sync::mpsc;

// Cancel-safe: the buffer lives OUTSIDE the select loop.
// If the recv branch fires, buf retains whatever was already read,
// and the next iteration continues filling it.
async fn good_example(
    stream: &mut BufReader<TcpStream>,
    rx: &mut mpsc::Receiver<u8>,
) -> std::io::Result<()> {
    let mut buf = [0u8; 1024];
    let mut filled = 0;

    loop {
        tokio::select! {
            n = stream.read(&mut buf[filled..]) => {
                // `read` (not `read_exact`) is cancel-safe: it either
                // reads some bytes or returns immediately with 0.
                filled += n?;
                if filled == buf.len() {
                    println!("buffer full: {:?}", &buf[..]);
                    filled = 0;
                }
            }
            msg = rx.recv() => {
                println!("got message: {:?}", msg);
            }
        }
    }
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not force async for CPU-bound work without I/O concurrency; prefer threads or Rayon when they fit the workload.

## verification
Add concurrency tests, cancellation tests, and runtime checks for backpressure or lock scope.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- async-bounded-channel
- async-no-lock-await
- async-select-racing
