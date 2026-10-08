# LTspice MCP

Active schematic: `simulations/tia_mcp_check/tia_check.asc`. Edit this file only; no independent test netlists.

| Item | Configuration |
| --- | --- |
| Server | Cognitohazard `ltspice-mcp==0.6.1`, stdio |
| Python environment | `local_only/ltspice_mcp/.venv` |
| Server configuration | `tools/ltspice-mcp.toml` |
| Client registration | `~/.codex/config.toml`, `mcp_servers.ltspice` |
| Simulator | `/Applications/LTspice.app`, installed version 17.2.4 |
| Symbol library | `~/Library/Application Support/LTspice/lib/sym` |
| File access | Project directory only; arbitrary-code MCP tool disabled |
| Generated data | Ignored `local_only/ltspice_mcp/store`, `state` and `.ltspice-mcp/` |

## Schematic Workflow

`inspect` reads components, pins, connections and the current file hash. `edit_schematic` changes the existing `.asc` transactionally; pass its last-read `expected_sha256`. A stale hash refuses the edit. `verify_circuit` checks symbols, layout and wiring. Edits made in the LTspice GUI must be saved before they can be read here.

Restart the MCP connection in the desktop app to discover the registered tools. Until then, the SDK client calls the same server without restarting the app:

```bash
local_only/ltspice_mcp/.venv/bin/python tools/ltspice_mcp_client.py inspect
local_only/ltspice_mcp/.venv/bin/python tools/ltspice_mcp_client.py verify
local_only/ltspice_mcp/.venv/bin/python tools/ltspice_mcp_client.py reference --query "add component wire pins"
```

The helper's edit target is fixed to `tia_check.asc`; edit ops require `--ops` and the `--expected-sha` obtained from inspection. `--dry-run` validates without writing.

## Simulation Boundary

The installed native Mac LTspice 17.2.4 does not support the library's command-line `.asc` netlist export. `.asc` editing is supported; fully automatic simulation of an edited `.asc` is not yet verified. Initially run this same schematic in LTspice, then use MCP `analyze_results` on its generated `.raw`. GUI automation also requires macOS Accessibility and Screen Recording permissions, which were pending during setup. The generated netlist is an execution artifact, not a separate design source. Do not claim a successful simulation from editing/geometry checks alone.

Verified: MCP handshake, tool discovery, ASC inspection, transactional edit dry-run and commit, symbol resolution, geometry checks, PNG rendering, and refusal of a path outside the project. The selected ASC now contains a generic TIA and parameterized APD/PIN equivalent models; see `simulations/tia_mcp_check/README.md`. Its native LTspice simulation is not yet verified.

Sources: [server](https://github.com/Cognitohazard/ltspice-mcp), [native-Mac batch/export limitations](https://spicelib.readthedocs.io/en/latest/_modules/spicelib/simulators/ltspice_simulator.html), [MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).
