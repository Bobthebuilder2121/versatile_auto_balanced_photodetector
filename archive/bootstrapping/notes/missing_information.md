# Project Direction and Minimum Requirements

This document defines a practical direction for the next project phase. The goal is not to collect many unrelated requirements, but to choose a small set of meaningful requirements that can be answered by simulation, measurement, or datasheet extraction.

## Recommended Direction

The project should focus on the following question:

**Can one auto-balanced photodetector front-end topology support different PIN and APD photodiodes by modeling the detector mainly as a photocurrent source in parallel with a capacitance, while maintaining useful bandwidth, CMRR, and bias stability?**

The circuit should therefore not be optimized for one exact diode at the beginning. Instead, use representative parameter ranges from available PIN and APD devices. As a first APD example, assume an InGaAs APD around 1550 nm, as suggested by the tutor.

## Candidate Devices

| Type | Candidate device | Role in project |
| --- | --- | --- |
| PIN | Hamamatsu G14942-32 | Example PIN detector |
| PIN | Hamamatsu G9801-22 | Example PIN detector |
| PIN | Roithner FCPD-55-C9 | Example PIN detector |
| APD | Hamamatsu G14858-0020AA | Example APD detector |

These devices should be used to define realistic parameter ranges, not to lock the whole design to a single part.

## Diode Parameter Table

The values below are extracted from the datasheets in `Diode_Datasheets/`.

| Device | Type | Material | Wavelength range / peak | Responsivity | Capacitance | Dark current | Bandwidth / rise time | Breakdown / max reverse voltage | Suggested simulation bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hamamatsu G14942-32 | PIN | InGaAs | 0.9-1.7 um / 1.55 um peak | 0.8 min, 0.95 typ A/W at 1.55 um | 1 typ, 1.5 max pF | 0.02 typ, 0.4 max nA | 2 GHz typ | 20 V max reverse voltage | Start with 5 V reverse bias |
| Hamamatsu G9801-22 | PIN | InGaAs | 0.9-1.7 um / 1.55 um peak | 0.8 min, 0.95 typ A/W at 1.55 um | 1 typ, 1.5 max pF | 0.02 typ, 0.4 max nA | 2 GHz typ | 20 V max reverse voltage | Start with 5 V reverse bias |
| Roithner FCPD-55-C9 | PIN | InGaAs | 0.85-1.7 um | 0.85 min, 0.90 typ A/W at 1550 nm | 0.5 typ, 1.0 max pF | 0.2 typ, 0.5 max nA | 3 GHz min; 0.3 ns max rise/fall | 45 V min breakdown; 15 V max reverse voltage | Start with 5 V reverse bias |
| Hamamatsu G14858-0020AA | APD | InGaAs | 0.95-1.7 um / 1.55 um peak | 0.65 min, 0.8 typ A/W at M=1 | 2.0 typ pF | 20 typ, 50 max nA | 0.9 GHz typ at M=10 | VBR 50 min, 65 typ, 80 max V | Check operation near selected APD bias |

For generic simulations, this suggests:

| Parameter | Useful first range | Brief explanation |
| --- | --- | --- |
| PIN capacitance | 0.5-1.5 pF | Use this as the input capacitance range for generic PIN simulations. |
| APD capacitance | about 2 pF | Use this as the first APD capacitance value; later it can be swept around this point. |
| PIN responsivity near 1550 nm | about 0.85-0.95 A/W | Converts optical power into photocurrent for PIN cases. |
| APD responsivity at M=1 near 1550 nm | about 0.65-0.8 A/W | Base responsivity before avalanche multiplication is applied. |
| PIN dark current at 5 V reverse bias | about 0.02-0.5 nA | Leakage current to include as a DC error/noise-related term. |
| APD dark current near high reverse bias | about 20-50 nA | APD leakage is much higher and matters for biasing and noise. |
| APD breakdown voltage range | 50-80 V, 65 V typical | Defines the high-voltage bias region for the APD case. |

## Minimum Requirements Table

This is the small requirements table that should guide the next work. Each row must lead to either a datasheet value, a simulation, or a measurement.

| ID | Requirement | First target / decision | How to solve it |
| --- | --- | --- | --- |
| R1 | Generic diode model | Current source + parallel capacitance | Extract capacitance and responsivity from datasheets |
| R2 | Diode capacitance range | Simulate low / typical / high capacitance | Build a small table from candidate PIN/APD datasheets |
| R3 | Photocurrent range | Use a current sweep first | Estimate from responsivity and assumed optical power |
| R4 | TIA bandwidth | Start with 1-10 MHz | Redesign `Rf` and `Cf`, then verify with AC/transient simulation |
| R5 | TIA gain | Avoid saturation while keeping useful output amplitude | Choose `Rf` from expected photocurrent range |
| R6 | Autobalance bandwidth | Cancel DC/common-mode drift without cancelling the signal | Sweep loop bandwidth and compare differential vs common-mode response |
| R7 | CMRR | Plot CMRR over frequency | Simulate equal input on both photodiodes and measure residual output |
| R8 | APD bias stability | Reverse bias should stay approximately constant | Plot APD reverse voltage during transient operation |
| R9 | Op-amp limits | No common-mode, supply, slew-rate, or output swing violations | Check operating points and transient maxima/minima |
| R10 | Layout sensitivity | Guarding and short high-impedance routing required | Document layout precautions before PCB design |

## What To Do Next

### 1. Define A Generic Simulation Diode

Use the extracted ranges to create two generic simulation cases:

| Simulation case | Meaning |
| --- | --- |
| Generic PIN case | Photocurrent source + representative PIN capacitance |
| Generic APD case | Photocurrent source + representative APD capacitance + reverse-bias requirement |

Do not yet model detailed optical physics. The first simulation goal is circuit behavior.

### 2. Redesign The TIA Around The Target Bandwidth

The current simulation uses approximately:

- `Rf = 1 kOhm`
- `Cf = 500 pF`
- bandwidth around `318 kHz`

This is below the stated 1-10 MHz target. The next step is to calculate and simulate new `Rf` and `Cf` values based on the diode capacitance range and desired transimpedance gain.

### 3. Simulate CMRR Versus Autobalance Bandwidth

This is probably the most important project-specific result.

Run simulations where both photodiodes receive the same common-mode input, then measure how much appears at the output. Repeat for several autobalance loop bandwidths.

The result should be a plot:

```text
CMRR [dB] vs frequency
```

This turns the vague requirement "good CMRR" into an actual design result.

### 4. Check That The Signal Is Not Cancelled

Apply differential input current:

```text
I1 = IDC + IAC
I2 = IDC - IAC
```

The output should contain the differential signal. If the autobalance loop is too fast, it may suppress part of the wanted signal. This test defines the upper useful bandwidth of the autobalance loop.

### 5. Check APD Bias Stability

For the APD case, plot the reverse voltage across the APD while the input signal changes.

The question is:

```text
Does the APD see an approximately constant reverse bias during operation?
```

If not, the APD gain will vary and distort the signal.

### 6. Validate Op-Amp Limits

For every promising simulation, check:

- op-amp input common-mode range
- local supply voltage difference
- output swing headroom
- slew-rate demand
- startup behavior

This is especially important because the TLV9162 has a limited maximum supply voltage.

## Good First Result For The Report

A strong first technical result would be:

1. A generic PIN/APD detector model derived from real candidate devices.
2. A redesigned TIA that reaches the chosen bandwidth target.
3. A CMRR-vs-frequency plot for different autobalance loop bandwidths.
4. A transient plot showing that the differential signal survives while DC/common-mode mismatch is reduced.
5. A bias-stability plot for the APD case.

If these five results are achieved, the project has a clear and defensible direction for the final paper.
