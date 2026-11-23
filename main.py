#!/usr/bin/env python3
"""Entrypoint for news-image-20261122 (round-3 radical build).

Copies the committed entry.png (drawn by draw.py, the build tool) into the
output directory after verifying it is a real PNG/JPEG within the 1 MiB cap.
Stdlib only, plain direct write, exit 0 on success. The image shows one day —
Sunday 22 November 2026: 20 dated stories, 7 regions, 11 illustrated, every
story drawn at poster scale so it reads at thumbnail size.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024  # 1 MiB competition cap


def main() -> int:
    # Round-3 note: the deliverable is the single committed page image;
    # verification below is deliberately strict (magic bytes + size cap)
    # so a corrupt or oversized render can never be shipped silently.
    with open(SRC, "rb") as fh:
        head = fh.read(8)
    size = os.path.getsize(SRC)
    is_png = head.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpeg = head.startswith(b"\xff\xd8\xff")
    if not (is_png or is_jpeg):
        print("entry.png is not a PNG/JPEG image", file=sys.stderr)
        return 1
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    os.chmod(dst, 0o644)
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
