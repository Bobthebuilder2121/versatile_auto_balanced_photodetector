# TMUX6136 IBIS Conversion Audit

Date: 2026-10-08. Original IBIS and previous LIB unchanged.
User approved correcting conversion and adding a datasheet-based analog extension.
Active `../tia_check.asc` now uses that extension; ADI copy remains
`../tia_check_ADG1236_alternative.asc`. See [extended model](extended_model.md).

## Installation

- Environment: project `.venv`, Python 3.14.
- Parser: `ecdtools==0.7.0`, `textparser==0.26.2`.
- Converter: `pybis2spice` 1.2, upstream commit
  `546618633b50d1bc0bdfd21e6250d835d122d59d`.
- Checkout: `.venv/src/pybis2spice`; editable pip installation.
- Upstream has no packaging configuration. Local `pyproject.toml` comes from
  `tools/pybis2spice_packaging.toml`; one reference-sign correction is tracked in
  `tools/pybis2spice_ground_reference.patch`.
- Existing NumPy 2.5.3 retained. No GUI/Qt dependencies required.

From the project root, rebuild the installation in a fresh environment:

```sh
git clone https://github.com/kamratia1/pybis2spice.git .venv/src/pybis2spice
git -C .venv/src/pybis2spice checkout 546618633b50d1bc0bdfd21e6250d835d122d59d
git -C .venv/src/pybis2spice apply ../../../tools/pybis2spice_ground_reference.patch
cp tools/pybis2spice_packaging.toml .venv/src/pybis2spice/pyproject.toml
.venv/bin/python -m pip install -e .venv/src/pybis2spice
.venv/bin/python tools/check_tmux_ibis_conversion.py
```

## Result

Generated 12 input subcircuits plus symbols: four supply variants, three corners.
Outputs in `pybis2spice/` use the corrected converter, but remain input-only models.
Machine-readable comparison: [audit.json](audit.json).

| Property | Previous LIB | pybis2spice output |
| --- | --- | --- |
| Ground/power clamp tables | 3 zero-current rows each | 99 original-current rows each |
| Package R/L/C and die C_comp | Present | Source values verified for all corners |
| Ground-clamp voltage axis, +/-15 V typical | Not meaningful; zero currents | Corrected; zero shift |
| Analog S-to-D path / R_ON / BBM / charge injection | Absent | Still absent |
| External supply terminals | Absent | Absent; fixed internal references |

## Corrected Converter Error

For a ground-clamp table, absolute input voltage is:

$$V_{absolute}=V_{table}+V_{GND\,reference}.$$

Upstream `define_pwr_and_gnd_clamps()` instead subtracts the reference.
For `input_15p0`, typical reference=-15 V, this shifts the table +30 V;
minimum/maximum shifts are +27/+33 V. For `input_5p0`, shifts are +10/+9/+11 V.
The local patch replaces subtraction with addition. Both clamp voltage axes and
both current columns now match the source in all 12 generated models.

The original IBIS also lists Vinl=2 V and Vinh=0.8 V, reversed relative to the
datasheet thresholds. No switching logic should be generated from these fields
without validating them. Original source data is unchanged; the extension uses
datasheet thresholds rather than these reversed IBIS fields.

## Verification

- All 12 model/corner conversions completed.
- Full current tables and numeric R/L/C values checked against parsed IBIS.
- Conversion-stage ASC SHA-256 unchanged; hashes in `audit.json` predate subsequent
  deliberate TI model integration.
- Upstream unit suite: 10 tests passed. `pip check`: passed.
- Input-only audit outputs are not a replacement for U3A/U3B. Native tests of the
  separate extended model are recorded in [extended_model.md](extended_model.md).

Sources: [pybis2spice](https://github.com/kamratia1/pybis2spice),
[ecdtools](https://github.com/eerimoq/ecdtools),
[IBIS 4.1 specification, GND Clamp Reference](https://ibis.org/ver4.1/ver4_1.txt),
[TMUX6136 datasheet](https://www.ti.com/lit/ds/symlink/tmux6136.pdf).

The sign correction is complete. The analog extension is explicitly approximate;
remaining validation is listed in its model notes.
