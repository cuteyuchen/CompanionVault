from __future__ import annotations

import argparse
import tarfile
import zipfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Package a PersonaDock standalone executable.")
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    binary = args.binary.resolve()
    output = args.output.resolve()
    if not binary.is_file():
        raise FileNotFoundError(binary)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.name.endswith(".tar.gz"):
        with tarfile.open(output, "w:gz") as archive:
            archive.add(binary, arcname=binary.name)
    elif output.suffix.lower() == ".zip":
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(binary, arcname=binary.name)
    else:
        raise ValueError("output must end with .tar.gz or .zip")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
