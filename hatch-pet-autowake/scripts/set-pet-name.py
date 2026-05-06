#!/usr/bin/env python3
import argparse
import json
import os
import shutil
from pathlib import Path


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def read_json(path: Path) -> dict:
    if not path.exists() or not path.read_text().strip():
        return {}
    return json.loads(path.read_text())


def write_json_with_backup(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text)
    path.with_suffix(path.suffix + ".bak").write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename/install a Codex custom pet package and select it.")
    parser.add_argument("--source-id", help="Existing pet folder id. Defaults to --pet-id.")
    parser.add_argument("--pet-id", required=True, help="ASCII folder/id for the pet, e.g. xiaoye.")
    parser.add_argument("--display-name", required=True, help="User-facing display name, e.g. 小椰.")
    parser.add_argument("--description", help="Pet description for pet.json.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing target folder.")
    args = parser.parse_args()

    home = codex_home()
    pets_dir = home / "pets"
    source_id = args.source_id or args.pet_id
    source_dir = pets_dir / source_id
    target_dir = pets_dir / args.pet_id
    pet_json = target_dir / "pet.json"

    if not source_dir.exists():
        raise SystemExit(f"Source pet folder not found: {source_dir}")

    if source_dir != target_dir:
        if target_dir.exists():
            if not args.force:
                raise SystemExit(f"Target exists: {target_dir}. Re-run with --force to replace it.")
            shutil.rmtree(target_dir)
        source_dir.rename(target_dir)

    if not (target_dir / "spritesheet.webp").exists():
        raise SystemExit(f"Missing spritesheet.webp in {target_dir}")

    data = read_json(pet_json)

    data["id"] = args.pet_id
    data["displayName"] = args.display_name
    data["description"] = args.description or data.get("description") or f"Custom Codex pet named {args.display_name}."
    data["spritesheetPath"] = "spritesheet.webp"
    pet_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    state_path = home / ".codex-global-state.json"
    state = read_json(state_path)
    atoms = state.setdefault("electron-persisted-atom-state", {})
    atoms["selected-avatar-id"] = f"custom:{args.pet_id}"
    write_json_with_backup(state_path, state)

    print(json.dumps({"ok": True, "pet_dir": str(target_dir), "pet_json": str(pet_json)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
