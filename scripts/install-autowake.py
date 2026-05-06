#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
from pathlib import Path


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def safe_label_id(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", value):
        raise SystemExit("pet-id must be lowercase ASCII letters, digits, and hyphens, starting with a letter or digit.")
    return value


def write_state(home: Path, pet_id: str) -> None:
    state_path = home / ".codex-global-state.json"
    state = {}
    if state_path.exists() and state_path.read_text().strip():
        state = json.loads(state_path.read_text())
    atoms = state.setdefault("electron-persisted-atom-state", {})
    atoms["selected-avatar-id"] = f"custom:{pet_id}"
    state["electron-avatar-overlay-open"] = True
    text = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
    state_path.write_text(text)
    state_path.with_suffix(state_path.suffix + ".bak").write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Install a macOS LaunchAgent that keeps a Codex custom pet awake.")
    parser.add_argument("--pet-id", required=True, help="Pet id under $CODEX_HOME/pets, e.g. xiaoye.")
    parser.add_argument("--interval", type=int, default=1, help="Seconds between state checks. Default: 1.")
    parser.add_argument("--no-load", action="store_true", help="Write files but do not load the LaunchAgent now.")
    args = parser.parse_args()

    pet_id = safe_label_id(args.pet_id)
    home = codex_home()
    pet_json = home / "pets" / pet_id / "pet.json"
    if not pet_json.exists():
        raise SystemExit(f"Missing pet package: {pet_json}")

    scripts_dir = home / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    script_path = scripts_dir / f"wake-{pet_id}.sh"
    launch_dir = Path.home() / "Library" / "LaunchAgents"
    launch_dir.mkdir(parents=True, exist_ok=True)
    label = f"com.codex.pet.{pet_id}.autowake"
    plist_path = launch_dir / f"{label}.plist"
    interval = max(1, args.interval)

    script = f"""#!/bin/zsh
set -euo pipefail

if [[ "${{1:-}}" == "--daemon" ]]; then
  while true; do
    "$0" || true
    sleep {interval}
  done
fi

STATE="${{CODEX_HOME:-$HOME/.codex}}/.codex-global-state.json"
PET_JSON="${{CODEX_HOME:-$HOME/.codex}}/pets/{pet_id}/pet.json"

[[ -f "$STATE" ]] || exit 0
[[ -f "$PET_JSON" ]] || exit 0

/usr/bin/python3 - "$STATE" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
raw = path.read_text().strip()
state = json.loads(raw) if raw else {{}}
atoms = state.setdefault("electron-persisted-atom-state", {{}})
changed = False

if atoms.get("selected-avatar-id") != "custom:{pet_id}":
    atoms["selected-avatar-id"] = "custom:{pet_id}"
    changed = True

if state.get("electron-avatar-overlay-open") is not True:
    state["electron-avatar-overlay-open"] = True
    changed = True

if changed:
    text = json.dumps(state, ensure_ascii=False, indent=2) + "\\n"
    path.write_text(text)
    path.with_suffix(path.suffix + ".bak").write_text(text)
PY
"""
    script_path.write_text(script)
    script_path.chmod(0o755)

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{script_path}</string>
    <string>--daemon</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>{home}/wake-{pet_id}.log</string>
  <key>StandardErrorPath</key>
  <string>{home}/wake-{pet_id}.err</string>
</dict>
</plist>
"""
    plist_path.write_text(plist)
    write_state(home, pet_id)

    if not args.no_load:
        uid = os.getuid()
        subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(plist_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(plist_path)], check=True)
        subprocess.run(["launchctl", "kickstart", "-k", f"gui/{uid}/{label}"], check=True)

    print(json.dumps({"ok": True, "label": label, "script": str(script_path), "plist": str(plist_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
