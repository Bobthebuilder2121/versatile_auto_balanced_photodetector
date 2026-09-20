# Architecture Update: Switching-Focused Photodetector Front-End

Meeting decision for the current architecture. The April 2026 bootstrap presentation is archived under `archive/bootstrapping/`.

## Main Architecture Decision

Bootstrapping is no longer part of the core architecture.

The project focus is now:

```text
APD/PIN input stage -> selectable input/switching mechanism -> interchangeable TIA -> interface/control logic
```

Autobalancing is no longer implemented by bootstrapped/flying rails. Instead, the system provides and regulates the diode bias voltage externally.

## Core Functional Blocks

| Block | Function | Design question |
| --- | --- | --- |
| Photodiode bias control | Sets PIN/APD reverse bias from the system side | How accurately and safely must diode bias be controlled? |
| Input switching mechanism | Selects operating mode or detector path | Relay, RF relay, analog switch, mux, diode switch, or transistor switch? |
| TIA | Converts photocurrent to voltage | Must be replaceable/interchangeable for different performance targets |
| Interface/control logic | Controls bias, switching, and readout mode | How are mode changes commanded and protected? |

## Updated Design Goal

Design should first be concrete enough to derive equations for one representative diode/system case, but the TIA block must remain replaceable.

Commercial reference detector mentioned:

```text
Thorlabs PDB570C
```

Use it as a reference system for equations and design constraints, not as a bare diode or a fixed circuit implementation. The first selected bare-diode pair is G14942-32 (PIN) and G14858-0020AA (APD).

## Required Analytical Work

Write equations for a simplified system first:

| Topic | Needed result |
| --- | --- |
| Photodiode current | Relation between optical power, responsivity, APD gain if applicable, and photocurrent |
| TIA gain | Relation between photocurrent, feedback resistor, feedback capacitor, and output voltage |
| Bandwidth | Approximate TIA bandwidth from feedback network and input capacitance |
| Bias voltage | Relation between system-provided bias and diode reverse voltage |
| Switching error | Estimate added resistance, capacitance, leakage, charge injection, and switching transient |

Purpose: make the design reasoning traceable.

## Switching Mechanism To Investigate

The core open design decision is the input switching mechanism.

| Option | Advantages | Risks / disadvantages |
| --- | --- | --- |
| Mechanical relay | Very low leakage, low capacitance, high isolation | Slow, bulky, contact bounce, limited lifetime |
| RF relay | Low parasitics, good high-frequency behavior, good isolation | Cost, size, drive requirements |
| Analog mux/switch | Compact, easy logic control, fast | Leakage, on-resistance, parasitic capacitance, charge injection |
| MOSFET/transistor switch | Customizable, compact | Nonlinear capacitance, leakage, bias-dependent behavior |
| Diode/Zener-based switching or protection | Simple protection/clamping possible | Not a clean signal switch; nonlinear and bias-dependent |

## Required Switching Evaluation

For each realistic switching option, document:

| Parameter | Why it matters |
| --- | --- |
| Off leakage current | Can look like photodiode dark current |
| On resistance | Adds error/noise and can disturb TIA input |
| Off capacitance | Loads the photodiode/TIA input and reduces bandwidth |
| Charge injection / glitching | Creates transients during mode switching |
| Isolation | Prevents inactive detector paths from affecting the active one |
| Bias voltage rating | Must survive APD/PIN reverse-bias conditions |
| Bandwidth / parasitic capacitance | Determines whether high-speed optical signals survive |

## Immediate Work Target

By September 24-25:

1. Recalculate the TIA for the new architecture.
2. Derive the simplified system equations.
3. Compare switching options scientifically.
4. Identify one concrete switching implementation to simulate.
5. Simulate performance with and without switching element.
6. Check switching glitching/transient behavior.

## Current Conclusion

The project is no longer primarily a bootstrapping architecture project.

The core technical question is now:

```text
Which switching/input-mode mechanism can be placed in front of an interchangeable TIA without degrading photodiode signal integrity, bias stability, leakage performance, or bandwidth?
```
