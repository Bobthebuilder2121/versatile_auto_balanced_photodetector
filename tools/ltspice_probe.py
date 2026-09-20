#!/usr/bin/env python3
"""Quickly inspect LTspice .raw/.log files for chat-based analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from PyLTSpice import LTSpiceLogReader, RawRead


def describe_raw(path: Path) -> None:
    raw = RawRead(str(path))
    names = raw.get_trace_names()
    print(f"RAW: {path}")
    print(f"  traces: {len(names)}")
    try:
        axis = raw.get_axis()
    except RuntimeError as exc:
        axis = None
        print(f"  axis: unavailable ({exc})")
    if axis is not None:
        print(f"  points: {len(axis)}")
        if len(axis):
            print(f"  axis: {axis[0]:.6g} to {axis[-1]:.6g}")
    print("  trace names:")
    for name in names:
        print(f"    {name}")


def describe_log(path: Path) -> None:
    print(f"LOG: {path}")
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or b"\x00" in raw[:200]:
        text = raw.decode("utf-16le", errors="ignore")
    else:
        text = raw.decode(errors="ignore")
    warnings = [line for line in text.splitlines() if "warning" in line.lower()]
    errors = [line for line in text.splitlines() if "error" in line.lower()]
    print(f"  warnings: {len(warnings)}")
    print(f"  errors: {len(errors)}")
    for line in warnings[:10]:
        print(f"    warning: {line}")
    for line in errors[:10]:
        print(f"    error: {line}")

    try:
        log = LTSpiceLogReader(str(path))
    except Exception as exc:
        print(f"  measurement parse: unavailable ({exc})")
        return

    steps = getattr(log, "stepset", None)
    if steps:
        print(f"  steps: {steps}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path, help="LTspice .raw or .log files")
    args = parser.parse_args()

    for file in args.files:
        suffix = file.suffix.lower()
        if suffix == ".raw":
            describe_raw(file)
        elif suffix == ".log":
            describe_log(file)
        else:
            print(f"Skipping unsupported file: {file}")


if __name__ == "__main__":
    main()
