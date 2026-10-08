# TMUX6136PWR Extended Model

**Local behavioral approximation, not an official TI SPICE model.**
Working point: +/-15 V, nominal 25 C, low-voltage reference/reset paths.
Never connect these switch ports to the +/-150 V diode bias rails.

| Source | Implemented |
| --- | --- |
| Original `input_15p0` IBIS, typical | 99 points per ground/power clamp; package R/L/C and die capacitance |
| Datasheet R_ON | 120 ohm at signal=0 V; two independent bidirectional paths |
| Datasheet capacitance | C_SOFF=2.4 pF, lumped selected-node C_ON=5.5 pF; SEL total=1.5 pF |
| Datasheet leakage, typical | IOFF=5 pA / ION=8 pA, explicit signed offsets |
| Datasheet logic | Low selects B; high selects A; 6 Mohm pull-down per SEL |
| BBM approximation | Turn-off delay=18 ns, turn-on delay=58 ns: 40 ns internal nonoverlap |
| Charge approximation | QJ=-0.4 pC at 0 V; signed packet into D, 5 ns smoothing |

## References And Assumptions

- Ground-clamp input uses `V(SEL_DIE,VSS)`. Power-clamp input uses
  `V(VDD,SEL_DIE)`; current positive into the component. Supply references are
  actual external nodes, not internal ideal supplies.
- IBIS thresholds are reversed. VTH=1.4 V is an assumed threshold within the
  datasheet's undefined interval 0.8--2 V, not a characterized threshold.
- Additional SEL capacitance is 1.5 pF minus IBIS package/die capacitance,
  avoiding double counting.
- Fixed analog capacitance partition: each S has 2.4 pF to GND; D has 3.1 pF
  to GND. At low frequency the selected S/D network has 5.5 pF. The drain split
  during BBM is assumed, not independently specified. No state-dependent charge
  capacitance is added on top of the explicit QJ packet.
- R_ON is constant. Voltage/temperature dependence and channel mismatch are not
  fitted. RON, CSOFF, CON, IOFF, ION, QJ and delays are per-instance parameters.
- Leakage polarity and dependence on voltage/temperature are not characterized
  by this model; use signed parameter sweeps for sensitivity.
- Opposite-edge charge polarity is assumed. Charge variation with source voltage
  and source/drain partition are not reconstructed from a single QJ test point.
- R_OFF=1e16 ohm is numerical isolation; it is not a resistance deduced from
  datasheet leakage. Analog package parasitics are not separately added to the
  measured terminal R_ON/capacitance values.
- Only ordinary passive resistor thermal noise is represented. Excess noise,
  leakage noise, crosstalk, supply-current dynamics, PSRR, analog ESD clamps and
  damage/protection behavior remain unvalidated. Do not use this model to certify
  RF bandwidth, absolute maximum ratings or a real APD's safety.

Sources: [TI datasheet, sections 5.5/5.6](https://www.ti.com/lit/ds/symlink/tmux6136.pdf),
[IBIS 4.1 reference/current conventions](https://ibis.org/ver4.1/ver4_1.txt).

## Files And Integration

- `../TMUX6136_extended.lib`: generated extended channel model.
- `../TMUX6136_SPDT.asy` and `../TMUX6136_SPDT_B.asy`: same terminal order;
  only the depicted contact differs. Installed under LTspice `lib/sym/Switches/`.
- `../tia_check.asc`: U3A/U3B replaced via MCP; existing signal/control wiring
  and user edits retained. Symbols depict CTRL=1. The unused U3B.SB remains open.
- `../tmux6136_model_tests.asc`: library-only regression fixture, not a separate
  detector design. Active detector source remains `tia_check.asc`.
- `tools/build_tmux6136_model.py`: deterministic model generator.
- `tools/test_tmux6136_model.py`: six source-data/reference/logic regressions.

From project root:

```sh
.venv/bin/python tools/check_tmux_ibis_conversion.py
.venv/bin/python tools/build_tmux6136_model.py
.venv/bin/python tools/test_tmux6136_model.py
```

## Validation Status

- Corrected conversion: 12/12 cases pass voltage-axis, current-table and R/L/C checks.
- Extended source-data/logical tests: 6/6 pass. Upstream unit tests: 10/10 pass.
- First native LTspice 17.2.4 fixture run completed at default TEMP=27 C with
  nominal 25 C model parameters (no temperature law implemented):

| Measurement | Native result |
| --- | ---: |
| R_ON, static 1 mA | 120 ohm |
| Loaded transition, R_L=300 ohm / C_L=35 pF | 65.4459 ns |
| Floating 1 nF charge-test output after opening A | +0.399033 mV |

The charge test is an opposite-edge consistency check, not a full reproduction
of the manufacturer's characterization fixture. Dedicated internal BBM/packet
measurements failed because internal data was not retained; save directives and
25 C were added for a rerun. That rerun and the updated detector simulation are
pending: native UI automation stopped responding. No full validation claimed.
Initial measured values are retained in [native_initial_results.json](native_initial_results.json).

MCP geometry/symbol checks pass apart from the intentional unused B contact.
An already-open ASC window can overwrite external MCP edits with its stale
in-memory version. Close/reopen `tia_check.asc` before rerunning; do not save an
old open copy over the updated source.
