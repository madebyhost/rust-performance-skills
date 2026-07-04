# Rust Performance Skills V4 Plugin And MCP Design

## Goal

Make `rust-performance-skills` visible in the local Codex plugin list and continue the project toward a safe, deterministic MCP surface without weakening the existing skill-first distribution.

## Approved Approach

Use Option A:

1. Add a plugin installation mode to `install.sh`.
2. Keep the current skills-only install targets intact.
3. Install the plugin into the Codex personal plugin layout.
4. Create or update the personal marketplace entry.
5. Install or refresh the plugin through `codex plugin add rust-performance-skills@personal` when the Codex CLI is available.
6. Start the MCP surface with deterministic offline tools only.

## Plugin Installation Contract

`install.sh` must support:

- `RUST_PERF_SKILLS_TARGET=plugin`
- `RUST_PERF_SKILLS_TARGET=all` including plugin install
- `RUST_PERF_SKILLS_PLUGIN_DIR` to override the plugin destination for tests and advanced users
- `RUST_PERF_SKILLS_MARKETPLACE` to override the marketplace file for tests and advanced users
- `RUST_PERF_SKILLS_SKIP_CODEX_ADD=1` to create files without invoking the Codex CLI

Default behavior:

- Plugin directory: `$HOME/plugins/rust-performance-skills`
- Marketplace file: `$HOME/.agents/plugins/marketplace.json`
- Marketplace name: `personal`
- Marketplace source path: `./plugins/rust-performance-skills`

The installer must copy this repository's plugin contents, not create an empty scaffold.

## Marketplace Contract

The marketplace entry must be:

```json
{
  "name": "rust-performance-skills",
  "source": {
    "source": "local",
    "path": "./plugins/rust-performance-skills"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Development"
}
```

If the marketplace file does not exist, create it with:

```json
{
  "name": "personal",
  "interface": {
    "displayName": "Personal"
  },
  "plugins": []
}
```

If an entry already exists, replace only the `rust-performance-skills` entry. Preserve all other marketplace entries.

## MCP Contract

The first MCP iteration must stay offline and deterministic. It can wrap existing scripts and static repository knowledge, but it must not add hooks, remote runtime launchers, `npx @latest`, credential handling, or network dependencies.

Initial MCP tools:

- `audit_rust_project`: run the same logic as `scripts/rust_project_audit.py`.
- `generate_quality_gates`: run the same logic as `scripts/generate_quality_gates.py`.
- `list_rust_skills`: return the packaged specialist skills with short descriptions.
- `rust_review_checklist`: return a checklist selected by project type and signals.

Implementation should prefer a small Python stdio MCP server if dependencies are already available or can be vendored lightly. If not, this iteration may ship a documented MCP scaffold plus tests for the config contract, but it must not introduce an opaque runtime.

## Safety Rules

- Do not add hooks.
- Do not add automatic shell commands beyond the explicit installer path.
- Do not add networked MCP dependencies.
- Do not modify global Claude or Codex settings outside the documented plugin marketplace path.
- Keep private project metadata out of commits, docs, generated files, and marketplace metadata.

## Testing

Add tests for:

- plugin install mode documented in README and install docs;
- marketplace JSON creation from an empty temporary home;
- marketplace JSON update preserving unrelated entries;
- plugin directory copy contract;
- `.mcp.json` declaring any MCP server only when the server file exists;
- MCP tool metadata or scaffold contract;
- distribution validator covering the new install and MCP files.

## Success Criteria

- `codex plugin list` can show `rust-performance-skills@personal` after installation.
- Existing skills-only installation remains supported.
- Distribution, skill, and plugin validators still pass.
- GitHub Actions passes.
- GitHub commits show `Mehdi AISSANI <contact@mehdiaissani.com>` as author and committer.
