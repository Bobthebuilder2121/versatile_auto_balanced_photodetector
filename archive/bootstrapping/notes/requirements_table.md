# Requirements Table

This table is meant to answer: **what direction should the project take, and what must be solved next?**

## Architecture Update

Bootstrapping is no longer part of the core architecture. The current focus is an externally biased photodiode front-end with an interchangeable TIA and a scientifically selected input switching mechanism.

| ID | Requirement | First target / decision | How to solve it |
| --- | --- | --- | --- |
| R1 | Generic diode model | Current source + parallel capacitance | Extract capacitance and responsivity from datasheets |
| R2 | Diode capacitance range | Simulate low / typical / high capacitance | Build a small table from candidate PIN/APD datasheets |
| R3 | Photocurrent range | Use a current sweep first | Estimate from responsivity and assumed optical power |
| R4 | TIA bandwidth | Recalculate for selected diode/input capacitance | Derive `Rf`, `Cf`, noise and bandwidth tradeoffs |
| R5 | TIA gain | Avoid saturation while keeping useful output amplitude | Choose `Rf` from expected photocurrent range |
| R6 | Input switching mechanism | Choose relay/RF relay/mux/transistor option | Compare leakage, capacitance, charge injection, isolation and voltage rating |
| R7 | Switching glitching | No unacceptable output transient during mode change | Simulate switch transition and measure recovery time |
| R8 | APD/PIN bias control | System provides diode bias externally | Define bias range, stability, protection and control interface |
| R9 | TIA interchangeability | TIA block must be replaceable | Define electrical interface: input node, bias constraints, output range |
| R10 | Op-amp/switch limits | No voltage, bandwidth, leakage or transient violations | Check operating points and transient maxima/minima |

## Candidate Devices

| Type | Candidate device | Use |
| --- | --- | --- |
| PIN | Hamamatsu G14942-32 | Extract realistic PIN parameters |
| PIN | Hamamatsu G9801-22 | Extract realistic PIN parameters |
| PIN | Roithner FCPD-55-C9 | Extract realistic PIN parameters |
| APD | Hamamatsu G14858-0020AA | Extract realistic APD parameters |

## Next Work

1. Recalculate the TIA for one concrete diode/system case.
2. Derive simplified equations for diode current, TIA gain, bandwidth and bias.
3. Compare switching mechanisms: relay, RF relay, analog mux, transistor switch, diode/Zener protection.
4. Simulate the selected switching element with and without switching transients.
5. Check bias stability, leakage, added capacitance and bandwidth loss.
