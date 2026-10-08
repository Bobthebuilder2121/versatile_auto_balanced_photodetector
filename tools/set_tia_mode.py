#!/usr/bin/env python3
"""Set the active ASC's Lorlin mode via revision-guarded MCP, without simulating."""

import argparse
import json
import logging
import math
import subprocess
from pathlib import Path

from spicelib import AscEditor
from spicelib.editor.base_schematic import TextTypeEnum


ROOT = Path(__file__).resolve().parents[1]
ASC = ROOT / "simulations/tia_mcp_check/tia_check.asc"
RUNTIME = ROOT / "local_only/ltspice_mcp/.venv/bin/python"
CLIENT = ROOT / "tools/ltspice_mcp_client.py"
SYMBOLS = Path.home() / "Library/Application Support/LTspice/lib/sym"
MODE_NAMES = ("I+ only", "I- only", "balanced", "autobalanced")


def requests(mode):
    if mode not in range(4):
        raise ValueError("Mode must be 0, 1, 2 or 3")
    return (int(mode != 1), int(mode != 0), int(mode == 3))


def call_client(*arguments):
    completed = subprocess.run(
        [str(RUNTIME), str(CLIENT), *arguments], cwd=ROOT,
        capture_output=True, text=True, timeout=180,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return json.loads(completed.stdout)


def make_ops(old, start, end, at_ms):
    requests(start)
    requests(end)
    if not math.isfinite(at_ms) or not 0 < at_ms < 30:
        raise ValueError("Switch time must be between 0 and 30 ms for this test")
    new = f".param MODE_START={start} MODE_END={end} T_SWITCH={at_ms:g}m"
    return [{"op": "remove_directive", "instruction": old},
            {"op": "add_directive", "instruction": new, "x": 32, "y": 1344}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", type=int, choices=range(4), nargs="?")
    parser.add_argument("--to", type=int, choices=range(4), dest="end")
    parser.add_argument("--at-ms", type=float, default=15)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()
    if args.mode is None and not args.show:
        parser.error("Supply a mode (0--3), or --show")
    if args.show and (args.mode is not None or args.end is not None):
        parser.error("--show cannot be combined with a mode change")
    if not args.show:
        try:
            make_ops("", args.mode, args.mode if args.end is None else args.end, args.at_ms)
        except ValueError as error:
            parser.error(str(error))
    if not RUNTIME.exists():
        raise RuntimeError("Project MCP runtime is missing")
    # Read the hash before the schematic. A concurrent edit then refuses the commit.
    inspected = call_client("inspect")
    item = next(item for item in inspected["results"] if item["kind"] == "components")
    if not item.get("ok"):
        raise RuntimeError("MCP could not inspect the active ASC")
    sha = item["data"]["sha256"]
    logging.getLogger("spicelib").setLevel(logging.ERROR)
    AscEditor.set_custom_library_paths(str(SYMBOLS), str(ASC.parent))
    editor = AscEditor(str(ASC))
    configs = [directive.text for directive in editor.directives
               if directive.type == TextTypeEnum.DIRECTIVE
               and directive.text.lower().startswith(".param mode_start=")]
    if len(configs) != 1:
        raise RuntimeError("Expected one Lorlin mode configuration in tia_check.asc")
    if args.show:
        print(configs[0])
        return
    end = args.mode if args.end is None else args.end
    ops = make_ops(configs[0], args.mode, end, args.at_ms)
    arguments = ["edit", "--expected-sha", sha, "--ops", json.dumps(ops)]
    if args.dry_run:
        arguments.append("--dry-run")
    result = call_client(*arguments)
    if result.get("failures"):
        raise RuntimeError(json.dumps(result["failures"]))
    expected = "not_committed" if args.dry_run else "committed"
    if result.get("commit_state") != expected:
        raise RuntimeError("MCP did not complete the requested edit")
    action = "Validated" if args.dry_run else "Configured"
    print(f"{action}: {args.mode} ({MODE_NAMES[args.mode]}) -> {end} ({MODE_NAMES[end]})"
          f" at {args.at_ms:g} ms")
    print("tia_check.asc only; reload it in LTspice and press Run. No simulation started.")


if __name__ == "__main__":
    main()
