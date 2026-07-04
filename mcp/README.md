# Optional MCP Roadmap

The v1 repository is skill-first. This directory documents MCP ideas that can be added without changing the public skill contract.

Useful future MCP tools:

- inspect Cargo release profiles and dependency feature flags;
- generate benchmark scaffolds for selected functions;
- parse Criterion output and summarize regressions;
- scan Rust diffs for hot-path red flags such as unbounded channels, clones, allocation, and blocking calls;
- produce latency-review checklists from project metadata.

Do not implement an MCP tool for advice that requires broad architectural judgment. Keep those decisions in the skill and references.
