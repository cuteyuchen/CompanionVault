from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test a PersonaDock standalone executable.")
    parser.add_argument("--binary", required=True, type=Path)
    args = parser.parse_args()

    binary = args.binary.resolve()
    if not binary.is_file():
        raise FileNotFoundError(binary)

    with tempfile.TemporaryDirectory(prefix="personadock-runtime-") as runtime_dir:
        runtime_root = Path(runtime_dir)
        skill_root = runtime_root / "installed-skills"

        subprocess.run([str(binary), "--help"], check=True, cwd=runtime_root)
        subprocess.run(
            [
                str(binary),
                "skill",
                "install",
                "--target",
                "generic",
                "--scope",
                "project",
                "--path",
                str(skill_root),
            ],
            check=True,
            cwd=runtime_root,
        )

        required = [
            "persona-builder/SKILL.md",
            "persona-builder/references/output-contract.md",
            "persona-builder/references/prompt-contract.md",
            "persona-builder/references/evidence-contract.md",
            "persona-builder/references/memory-contract.md",
        ]
        for relative in required:
            path = skill_root / relative
            if not path.is_file():
                raise FileNotFoundError(path)

        skill_text = (skill_root / "persona-builder/SKILL.md").read_text(encoding="utf-8")
        for marker in ("Create mode", "Distill mode", "Hybrid mode", "Refine mode"):
            if marker not in skill_text:
                raise AssertionError(f"missing Skill marker: {marker}")

    print(f"Verified standalone binary: {binary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
