#!/usr/bin/env python3
"""Call the registered MCP server on the project's selected .asc schematic."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import tomllib

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
TARGET = "simulations/tia_mcp_check/tia_check.asc"


async def main(args: argparse.Namespace) -> None:
    settings = tomllib.loads((Path.home() / ".codex/config.toml").read_text())
    server = settings["mcp_servers"]["ltspice"]
    if not server.get("enabled", True) or Path(server["cwd"]).resolve() != ROOT:
        raise RuntimeError("Registered LTspice MCP server is disabled or targets another project")
    params = StdioServerParameters(
        command=server["command"], args=server["args"], cwd=ROOT,
        env=dict(os.environ, **server.get("env", {})),
    )
    if args.action == "inspect":
        tool, request = "inspect", {"queries": [
            {"kind": "capabilities"},
            {"kind": "components", "path": TARGET, "detail": "full"},
        ]}
    elif args.action == "reference":
        tool, request = "inspect", {"queries": [
            {"kind": "reference", "query": args.query or "edit_schematic", "limit": 2},
        ]}
    elif args.action == "verify":
        tool, request = "verify_circuit", {
            "path": TARGET, "checks": ["symbols", "layout", "quality"],
        }
    else:
        if not args.ops or not args.expected_sha:
            raise ValueError("edit requires --ops JSON and --expected-sha from the last inspect")
        ops = json.loads(args.ops)
        if not isinstance(ops, list):
            raise ValueError("--ops must be a JSON list")
        tool, request = "edit_schematic", {
            "target": TARGET, "base": "existing", "expected_sha256": args.expected_sha,
            "ops": ops, "dry_run": args.dry_run, "return_views": ["touched", "pin_legend"],
        }
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer, read_timeout_seconds=180) as session:
            await session.initialize()
            result = (await session.call_tool(tool, request)).model_dump()
    if result.get("is_error"):
        raise RuntimeError(json.dumps(result["content"]))
    data = result.get("structured_content")
    if not isinstance(data, dict):
        raise RuntimeError("MCP server returned no structured result")
    print(json.dumps(data, indent=2))
    if data.get("error_count", 0) or data.get("failures") or data.get("outcome") in {"failed", "error", "conflict"}:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "verify", "edit", "reference"], nargs="?", default="inspect")
    parser.add_argument("--query")
    parser.add_argument("--ops", help="JSON edit-op list; the target path is fixed")
    parser.add_argument("--expected-sha", help="SHA-256 reported by the last inspect; prevents overwriting newer edits")
    parser.add_argument("--dry-run", action="store_true")
    asyncio.run(main(parser.parse_args()))
