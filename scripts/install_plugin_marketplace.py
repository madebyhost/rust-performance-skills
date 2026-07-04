#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path


PLUGIN_NAME = "rust-performance-skills"
ENTRY = {
    "name": PLUGIN_NAME,
    "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Development",
}


def copy_plugin(source: Path, plugin_dir: Path) -> None:
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)
    ignore = shutil.ignore_patterns(".git", ".worktrees", "__pycache__", "*.pyc")
    shutil.copytree(source, plugin_dir, ignore=ignore)


def load_marketplace(path: Path) -> dict:
    if not path.exists():
        return {"name": "personal", "interface": {"displayName": "Personal"}, "plugins": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("marketplace.json must be an object")
    data.setdefault("name", "personal")
    data.setdefault("interface", {"displayName": "Personal"})
    data.setdefault("plugins", [])
    return data


def update_marketplace(path: Path) -> None:
    data = load_marketplace(path)
    plugins = data["plugins"]
    if not isinstance(plugins, list):
        raise ValueError("marketplace plugins must be an array")
    for index, entry in enumerate(plugins):
        if isinstance(entry, dict) and entry.get("name") == PLUGIN_NAME:
            plugins[index] = ENTRY
            break
    else:
        plugins.append(ENTRY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install rust-performance-skills into the Codex personal plugin marketplace.")
    parser.add_argument("--source", default=".", help="repository source path")
    parser.add_argument("--plugin-dir", required=True, help="destination plugin directory")
    parser.add_argument("--marketplace", required=True, help="marketplace.json path")
    args = parser.parse_args()
    copy_plugin(Path(args.source).resolve(), Path(args.plugin_dir).expanduser().resolve())
    update_marketplace(Path(args.marketplace).expanduser().resolve())
    print(f"installed {PLUGIN_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
