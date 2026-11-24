#!/usr/bin/env python3
"""Copy the finished front page to make.fun's output directory.

The entry image is a one-page newspaper that sums up the world news
of Monday, 23 November 2026: Nvidia brings back Jensen Huang as its
chief executive (shares jump 31%), seven more photo stories from the
same day, and a three-item ticker at the foot of the page. The image
is already drawn and stored next to this file as entry.png; this
program only moves it, byte for byte, to $MAKEFUN_OUTPUT_DIR/entry.png.

Because the copy is a plain byte copy with no clock, random input,
or other varying data involved, running the program twice over the
same source always writes an identical file. That is what makes the
build reproducible.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1
    if os.path.getsize(source) == 0:
        print(f"error: source image is empty: {source}", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)

    shutil.copyfile(source, target)

    if os.path.getsize(target) != os.path.getsize(source):
        print(
            f"error: copied file size {os.path.getsize(target)} does not "
            f"match source size {os.path.getsize(source)}",
            file=sys.stderr,
        )
        return 1

    print(f"copied {source} -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
