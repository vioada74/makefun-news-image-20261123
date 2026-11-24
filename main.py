#!/usr/bin/env python3
"""Place the finished front page where make.fun will read it.

The one-page newspaper for Monday, 23 November 2026 is already drawn
and saved as entry.png in the same folder as this script. This program
only copies that file, byte for byte, to $MAKEFUN_OUTPUT_DIR/entry.png.

Copying bytes does not depend on the clock or on random data, so two
runs over the same source always write an identical file.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

IMAGE = "entry.png"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def die(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def main():
    here = Path(__file__).resolve().parent
    source = here / IMAGE

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return die("MAKEFUN_OUTPUT_DIR is not set")

    if not source.is_file():
        return die(f"no {IMAGE} found next to this script")
    if source.stat().st_size == 0:
        return die(f"{IMAGE} is empty")

    target_dir = Path(out_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE
    shutil.copyfile(source, target)

    if target.stat().st_size != source.stat().st_size:
        return die("copy size differs from the source size")
    if _sha256(target) != _sha256(source):
        return die("copy contents differ from the source")

    print(f"copied {source} to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
