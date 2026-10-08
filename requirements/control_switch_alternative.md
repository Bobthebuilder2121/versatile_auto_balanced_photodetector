# Control Switch Alternative

Primary: **TMUX6136PWR** (TI). Alternative: **ADG1236YRUZ** (Analog Devices).
Use the TSSOP-16 version, not the differently pinned LFCSP version.

| Parameter | TMUX6136PWR | ADG1236YRUZ |
| --- | ---: | ---: |
| Function | 2 independent SPDT | 2 independent SPDT |
| Package / pitch | TSSOP-16 / 0.65 mm | TSSOP-16 / 0.65 mm |
| R_ON, typical | 120 ohm | 120 ohm |
| C_ON, typical | 5.5 pF | 3.5 pF |
| C_S(OFF), typical | 2.4 pF | 1.3 pF |
| Charge injection, typical | -0.4 pC | -1 pC |
| On leakage, maximum at 25 C | 0.06 nA | 0.2 nA |
| Break-before-make | Yes | Yes |
| Logic low / high thresholds | <=0.8 V / >=2.0 V | <=0.8 V / >=2.0 V |

R_ON/capacitance/charge figures: +/-15 V supplies; R_ON test voltages differ
(TI 0 V, ADI +/-10 V). ADI leakage is specified at +/-16.5 V; TI at +/-15 V.
These are datasheet test values, not interchangeable worst-case guarantees.

## Verified Pin Mapping

| TSSOP pin | Both devices |
| --- | --- |
| 1 / 9 | Channel 1 / 2 control (TI SEL, ADI IN) |
| 2 / 3 / 4 | S1A / D1 / S1B |
| 5 / 6 | VSS / GND |
| 10 / 11 / 12 | S2A / D2 / S2B |
| 13 | VDD |
| 7, 8, 14, 15, 16 | NC; leave unconnected |

Both: logic 0 selects B, logic 1 selects A. Supply, signal and logic pins
match. In this design use +/-15 V switch supplies and 0/3.3 V control.
These switches operate in the low-voltage PI/reference path, before HV level translation.

Sources: [TI datasheet](https://www.ti.com/lit/ds/symlink/tmux6136.pdf),
[ADI datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/adg1236.pdf).

## LTspice Integration

`simulations/tia_mcp_check/tia_check.asc`: U3A and U3B are the two channels of
one ADG1236 package, represented by two instances of the official single-channel
LTspice symbol/model. `ADG1236.sub` is the installed vendor model, copied unchanged
beside the ASC. It is encrypted; internal model coverage cannot be audited here.
An ADG1236 simulation does not verify the TMUX6136's behavior or package crosstalk.

The manufacturer lists both a native LTspice model and a downloadable
[SPICE macro model](https://www.analog.com/en/products/adg1236.html#tools-and-simulations).

| CTRL | S1 | S2 | VPI after, measured |
| --- | --- | --- | ---: |
| 0 | Vref0=0 V | PI output to summing input | -0.939 mV |
| 1 | PI output | Reset contact disconnected | -1.38734 V |

Native LTspice 17.2.4, 2026-10-08: both 30 ms cases completed; source stepping
converged. CTRL=1: final TIA DC=-15.98 uV, VOUT=0.997618 Vpp, upper bias=149.8 V.
CTRL=0: command remains 0 V; upper bias is about 148.417 V due to MOSFET V_GS.
RCMD=1 kohm / CCMD=100 nF retain the command filter. Tests verify static mode
selection and the fictive current-mismatch response, not a timed mode transition.
