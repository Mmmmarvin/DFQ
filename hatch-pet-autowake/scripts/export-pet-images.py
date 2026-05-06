#!/usr/bin/env python3
import argparse
import os
import shutil
import time
from pathlib import Path


IMAGE_EXTS = {".png", ".webp", ".jpg", ".jpeg", ".gif"}


def copytree_if_exists(src: Path, dst: Path) -> None:
    if src.exists():
        shutil.copytree(src, dst, dirs_exist_ok=True)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for n in range(2, 1000):
        candidate = path.with_name(f"{path.name}-{n}")
        if not candidate.exists():
            return candidate
    raise SystemExit(f"Could not choose a unique output folder near: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export hatch-pet image artifacts into a tidy folder.")
    parser.add_argument("--run-dir", required=True, help="Hatch run directory.")
    parser.add_argument("--pet-id", required=True, help="Installed pet id under $CODEX_HOME/pets.")
    parser.add_argument("--output-dir", required=True, help="Destination folder.")
    parser.add_argument("--include-generated-candidates", action="store_true", help="Also copy recent $CODEX_HOME/generated_images candidates.")
    parser.add_argument("--generated-candidate-hours", type=float, default=12, help="How far back to collect generated candidates. Default: 12.")
    parser.add_argument("--force", action="store_true", help="Replace --output-dir if it already exists.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser()
    out = Path(args.output_dir).expanduser()
    home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    pet_dir = home / "pets" / args.pet_id

    if not run_dir.exists():
        raise SystemExit(f"Run dir not found: {run_dir}")

    if out.exists() and args.force:
        shutil.rmtree(out)
    elif out.exists():
        out = unique_path(out)
    out.mkdir(parents=True)

    copytree_if_exists(run_dir / "final", out / "final")
    copytree_if_exists(run_dir / "decoded", out / "decoded-row-strips")
    copytree_if_exists(run_dir / "frames", out / "extracted-frames")
    copytree_if_exists(run_dir / "qa", out / "qa")
    copytree_if_exists(run_dir / "references", out / "references")
    copytree_if_exists(pet_dir, out / "installed-pet-package")

    if args.include_generated_candidates:
        dest = out / "original-generated-candidates"
        dest.mkdir(exist_ok=True)
        cutoff = time.time() - max(args.generated_candidate_hours, 0) * 3600
        for p in (home / "generated_images").glob("**/*"):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS and p.stat().st_mtime >= cutoff:
                shutil.copy2(p, dest / p.name)

    shutil.make_archive(str(out), "zip", out.parent, out.name)
    count = sum(1 for p in out.rglob("*") if p.is_file())
    print({"ok": True, "output_dir": str(out), "zip": str(out) + ".zip", "files": count})


if __name__ == "__main__":
    main()
