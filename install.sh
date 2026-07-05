#!/bin/sh
set -eu

REPO_URL="https://github.com/madebyhost/rust-performance-skills"
REF="${RUST_PERF_SKILLS_REF:-main}"
TARGET="${RUST_PERF_SKILLS_TARGET:-auto}"
PREFIX="${RUST_PERF_SKILLS_PREFIX:-$HOME}"
PLUGIN_DIR="${RUST_PERF_SKILLS_PLUGIN_DIR:-$HOME/plugins/rust-performance-skills}"
MARKETPLACE="${RUST_PERF_SKILLS_MARKETPLACE:-$HOME/.agents/plugins/marketplace.json}"
AGENTS="${RUST_PERF_SKILLS_AGENTS:-auto}"
PROJECT_DIR="${RUST_PERF_SKILLS_PROJECT_DIR:-$PWD}"
AGENT_BUNDLE_DIR="${RUST_PERF_SKILLS_AGENT_BUNDLE_DIR:-$PREFIX/.agents/rust-performance-skills}"
CLAUDE_MARKETPLACE="${RUST_PERF_SKILLS_CLAUDE_MARKETPLACE:-madebyhost-rust-performance}"
# RUST_PERF_SKILLS_SKIP_CLAUDE_ADD=1 skips `claude plugin marketplace add` and `claude plugin install`.
# RUST_PERF_SKILLS_FORCE_CLAUDE_ADD=1 allows tests or custom prefixes to force Claude CLI registration.
# RUST_PERF_SKILLS_CLAUDE_CLEAN_STANDALONE=1 removes older ~/.claude/skills/rust-* standalone copies.

tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT INT TERM

archive="$tmp_dir/rust-performance-skills.tar.gz"
src_dir="$tmp_dir/src"

download() {
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$1" -o "$archive"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$archive" "$1"
  else
    echo "error: curl or wget is required" >&2
    exit 1
  fi
}

if [ "${RUST_PERF_SKILLS_SKIP_DOWNLOAD:-0}" = "1" ]; then
  src_dir="$(pwd)"
else
  download "$REPO_URL/archive/refs/heads/$REF.tar.gz"
  mkdir -p "$src_dir"
  tar -xzf "$archive" -C "$src_dir" --strip-components 1
fi

install_skills() {
  dest="$1"
  mkdir -p "$dest"
  cp -R "$src_dir"/skills/rust-* "$dest/"
  echo "installed rust-performance-engineering skills into $dest"
}

install_plugin() {
  python3 "$src_dir/scripts/install_plugin_marketplace.py" \
    --source "$src_dir" \
    --plugin-dir "$PLUGIN_DIR" \
    --marketplace "$MARKETPLACE"
  if [ "${RUST_PERF_SKILLS_SKIP_CODEX_ADD:-0}" != "1" ] && command -v codex >/dev/null 2>&1; then
    codex plugin add rust-performance-skills@personal
  else
    echo "skipped: codex plugin add rust-performance-skills@personal"
  fi
}

install_agent_adapters() {
  selected_agents="$1"
  python3 "$src_dir/scripts/install_agent_adapters.py" \
    --source "$src_dir" \
    --prefix "$PREFIX" \
    --project-dir "$PROJECT_DIR" \
    --bundle-dir "$AGENT_BUNDLE_DIR" \
    --claude-marketplace "$CLAUDE_MARKETPLACE" \
    --agents "$selected_agents"
}

case "$TARGET" in
  auto)
    install_agent_adapters "$AGENTS"
    if [ "${RUST_PERF_SKILLS_SKIP_CODEX_ADD:-0}" != "1" ] && command -v codex >/dev/null 2>&1; then
      install_plugin
    fi
    ;;
  agents)
    install_agent_adapters "$AGENTS"
    ;;
  codex)
    install_skills "$PREFIX/.codex/skills"
    ;;
  claude)
    install_agent_adapters claude
    ;;
  claude-skills)
    install_skills "$PREFIX/.claude/skills"
    ;;
  local)
    install_skills "$PWD/.agents/skills"
    ;;
  plugin)
    install_plugin
    ;;
  all)
    install_skills "$PREFIX/.codex/skills"
    install_skills "$PWD/.agents/skills"
    install_plugin
    install_agent_adapters "${RUST_PERF_SKILLS_AGENTS:-all}"
    ;;
  gemini|cursor|windsurf|cline|roo|kilocode|antigravity|pi|hermes|opencode|openclaw|ollama|copilot)
    install_agent_adapters "$TARGET"
    ;;
  *)
    echo "error: RUST_PERF_SKILLS_TARGET must be auto, agents, all, codex, claude, claude-skills, local, plugin, gemini, cursor, windsurf, cline, roo, kilocode, antigravity, pi, hermes, opencode, openclaw, ollama, or copilot" >&2
    exit 2
    ;;
esac

echo "invoke with: Use \$rust-performance-engineering, or /rust-performance-skills:rust-performance-engineering in Claude plugin mode."
