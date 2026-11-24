#!/usr/bin/env python3
"""Houseplant Out-of-Office — make.fun entry.

Writes one out-of-office auto-reply, as if a houseplant sent it, to
``entry.txt`` inside the make.fun output directory.

The line is the whole entry: a fern that went on strike in March after
months of being ignored, now on "photosynthesis leave". The gate only
accepts 1-120 UTF-8 characters, so the program asserts the length and
verifies the file it wrote by reading the bytes back.

The em dash in the line is U+2014; the file is written as UTF-8 with no
trailing newline, so the bytes on disk are exactly the line itself.
"""

import os
import sys

LINE = "Out of office: the fern went on strike in March. No water, no replies — management calls it photosynthesis leave."

# The grader's output directory. ``MAKEFUN_OUTPUT_DIR`` stands in for it
# outside the grader; when neither is usable we fall back to ./output.
DEFAULT_OUTPUT_DIR = "/output"
FALLBACK_OUTPUT_DIR = os.path.join(os.getcwd(), "output")


def _usable(directory):
    """True when ``directory`` exists (or can be created) and is writable."""
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        return False
    return os.access(directory, os.W_OK)


def resolve_output_dir():
    """Pick the first usable output directory, in priority order."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append(DEFAULT_OUTPUT_DIR)
    candidates.append(FALLBACK_OUTPUT_DIR)
    for directory in candidates:
        if _usable(directory):
            return directory
    # Last resort: let the open() below raise a clear error.
    return candidates[0]


def main():
    assert 1 <= len(LINE) <= 120, "line must be 1-120 characters"
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    with open(path, "rb") as f:
        data = f.read()
    assert data == LINE.encode("utf-8"), "read-back bytes differ from LINE"
    assert not data.endswith(b"\n"), "entry.txt must not end with a newline"
    print(LINE)
    print("characters: %d" % len(LINE))
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
