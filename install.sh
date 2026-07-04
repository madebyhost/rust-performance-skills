#!/bin/sh
set -eu

REPO_URL="https://github.com/madebyhost/rust-performance-skills"
REF="${RUST_PERF_SKILLS_REF:-main}"
TARGET="${RUST_PERF_SKILLS_TARGET:-all}"
PREFIX="${RUST_PERF_SKILLS_PREFIX:-$HOME}"
PLUGIN_DIR="${RUST_PERF_SKILLS_PLUGIN_DIR:-$HOME/plugins/rust-performance-skills}"
MARKETPLACE="${RUST_PERF_SKILLS_MARKETPLACE:-$HOME/.agents/plugins/marketplace.json}"

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

case "$TARGET" in
  codex)
    install_skills "$PREFIX/.codex/skills"
    ;;
  claude)
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
    install_skills "$PREFIX/.claude/skills"
    install_skills "$PWD/.agents/skills"
    install_plugin
    ;;
  *)
    echo "error: RUST_PERF_SKILLS_TARGET must be all, codex, claude, local, or plugin" >&2
    exit 2
    ;;
esac

echo "invoke with: Use \$rust-performance-engineering to review this Rust project."
