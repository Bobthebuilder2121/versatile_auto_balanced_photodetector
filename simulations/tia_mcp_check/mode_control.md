# Four-mode control

Active schematic: `tia_check.asc`. Lorlin CK1031 positions are modeled as ideal decoded commands, not mechanical contacts.

| Mode | Upper relay | Lower relay | PI reference | PI reset |
|---|---|---|---|---|
| 0: I+ | Closed | Open | Fixed 0 V | Active |
| 1: I- | Open | Closed | Fixed 0 V | Active |
| 2: Balanced | Closed | Closed | Fixed 0 V | Active |
| 3: Autobalanced | Closed | Closed | PI output | Released |

## Commands

Run from the project root:

```sh
# Fixed mode, e.g. balanced
.venv/bin/python tools/set_tia_mode.py 2

# Balanced -> autobalanced at 15 ms
.venv/bin/python tools/set_tia_mode.py 2 --to 3 --at-ms 15

# Inspect saved configuration
.venv/bin/python tools/set_tia_mode.py --show
```

Use `--dry-run` to validate an edit without saving it. The script changes only the mode parameter directive in the active ASC, through revision-guarded MCP. It does not start a simulation. In LTspice, reload using **File -> Revert to Saved**, then **Run**; do not save a stale open schematic over the script's edit.

## Model Limits

- `KPLUS/KMINUS`: Coto 9012-12-10, functional approximation, not a manufacturer model. Coil: 12 V / 750 ohm; contact: 0.12 ohm ON, 1e12 ohm OFF, 0.7 pF across contacts. Contact-to-coil capacitance: assumed split of the specified total 1.4 pF.
- Relay delay: 350 us ON, 100 us OFF. No contact bounce, coil inductance or flyback-driver model. Timing values are not a worst-case sequencing guarantee.
- `AB_DELAY=400u`: provisional enable delay; AB disables immediately. TMUX channel A selects fixed reference or PI; channel B resets/releases PI.
- `MODE_START/MODE_END/T_SWITCH`: one scheduled transition, not live control. Initial mode is also the operating-point state.
- Existing generic diode, fictive bias sensitivity, TIA, buffer, LPF, PI and post-regulator remain unchanged. `V1=0 V` measures TIA input current.
- Unbalanced operation: approximately 1 mA DC through 5 kohm can reach the +/-5 V amplifier limit. Mode selection does not guarantee unclipped output or APD protection.
- For physical operation, relay drivers, contact bounce/debounce, supply limits and controller enable/reset sequencing still require verification.

Relay parameters: [Coto 9011/9012/9117 datasheet](https://www.cotorelay.com/datasheets/Classic-9011-9012-9117-Reed-Relay.pdf).

## Verification

2026-10-08: ten Python regressions pass (four mode-control tests, six TI model tests). Native LTspice 17.2.4 resolved all models and found the operating point using Gmin stepping. The 2 -> 3 transient was manually stopped at 1.65813 ms after 136.53 s; the 15 ms transition and final measurements are **not verified**. Current RAW/LOG contain that partial run, not the previous completed baseline. Runtime optimization is still required before evaluating the transition.
