# TIA Model Equations

Source: `literature/transimpedance calc.pdf`, chapter 5, Transimpedance Amplifier Specifications.

## 1. Signal Definition

Use the intrinsic photodiode photocurrents as the input signal.

```text
mode        S+   S-   input current
I+          1    0    i_in = +i_ph+
I-          0    1    i_in = -i_ph-
balanced    1    1    i_in = i_ph+ - i_ph-
```

Small-signal transimpedance:

```math
Z_T(s)=\frac{V_{out}(s)}{I_{in}(s)}
```

Low-frequency ideal TIA:

```math
V_{out}\approx V_{ref}-I_{in}R_F
```

With maximum input current:

```math
I_{in,max}=1\,\mathrm{mA}
```

Target output swing:

```math
V_{out,target}=1\,\mathrm{V_{pp}}
```

Output swing constraint:

```math
R_F \leq \frac{V_{out,lin}}{I_{in,max}}
```

First design value:

```math
R_F\approx\frac{1\,\mathrm{V_{pp}}}{1\,\mathrm{mA_{pp}}}=1\,\mathrm{k\Omega}
```

Examples:

| Available linear output swing | Maximum \(R_F\) for \(1\,\mathrm{mA}\) |
|---:|---:|
| \(1\,\mathrm{V}\) | \(1\,\mathrm{k\Omega}\) |
| \(2\,\mathrm{V}\) | \(2\,\mathrm{k\Omega}\) |
| \(5\,\mathrm{V}\) | \(5\,\mathrm{k\Omega}\) |

This is the first hard limit: with \(1\,\mathrm{mA}\) maximum current and \(1\,\mathrm{V_{pp}}\) output target, the first TIA gain estimate is \(R_F=1\,\mathrm{k\Omega}\).

## 2. Photodiode Model

For TIA dimensioning each diode is modeled as:

```text
photocurrent source || junction capacitance || shunt resistance
```

```math
i_{ph}=R(\lambda)\,P_{opt}\,M
```

where:

| Symbol | Meaning |
|---|---|
| \(R(\lambda)\) | responsivity at wavelength |
| \(P_{opt}\) | incident optical power |
| \(M\) | APD multiplication factor; \(M=1\) for PIN |
| \(C_J\) | diode junction capacitance |
| \(R_{SH}\) | diode shunt resistance, if specified |
| \(I_D\) | dark current |

Use variable capacitance:

```math
C_J \in [C_{J,min}, C_{J,max}]
```

Initial concrete values:

| Diode | \(C_J\) for first model |
|---|---:|
| Hamamatsu G14858-0020AA APD | \(2.0\,\mathrm{pF}\) typ |
| Hamamatsu G14942-32 PIN | \(1.0\,\mathrm{pF}\) typ, \(1.5\,\mathrm{pF}\) max |

## 3. Switch Equivalent Model

Each photodiode branch uses one controlled switch path between diode signal node and TIA summing node.

### ON State

```text
diode node -- R_on -- L_on -- TIA summing node
                  |
                C_on
                  |
                 GND
```

Model terms:

```math
Z_{sw,on}(s)=R_{on}+sL_{on}
```

```math
Y_{sw,on,par}(s)=sC_{on}+G_{leak,on}
```

For a relay, \(R_{on}\) and \(L_{on}\) dominate.  
For a CMOS analog switch, \(R_{on}\), \(C_{on}\), leakage and charge injection dominate.

### OFF State

```text
diode node -- C_off -- TIA summing node
diode node -- R_off -- TIA summing node
```

Model terms:

```math
Y_{sw,off}(s)=sC_{off}+G_{off}
```

Equivalent off-branch capacitance seen by the TIA input, if the inactive diode node is not hard-grounded:

```math
C_{off,eq}\approx \frac{C_{off}C_J}{C_{off}+C_J}
```

If the inactive diode signal node is switched to ground:

```math
C_{off,eq}\approx C_{off}
```

because the far side of the off capacitance is now AC-grounded.

Switching transient:

```math
\Delta V_{in}\approx \frac{Q_{inj}}{C_{in,total}}
```

Output recovery is then evaluated in transient simulation with the actual TIA:

```math
V_{out,glitch}(t)=\mathcal{L}^{-1}\{Z_T(s)I_{glitch}(s)\}
```

where \(Q_{inj}\) is relevant mainly for semiconductor switches. For relays, evaluate contact bounce and settling instead.

## 4. Total Input Capacitance

The TIA bandwidth and noise must be evaluated with the capacitance actually seen at the summing node.

```math
C_{in,total}=C_{opamp}+C_{PCB}+C_{mode}+C_{off,eq}
```

Mode-dependent connected capacitance:

```math
C_{mode}=
\begin{cases}
C_{J+}+C_{sw,on+}, & I+\\
C_{J-}+C_{sw,on-}, & I-\\
C_{J+}+C_{J-}+C_{sw,on+}+C_{sw,on-}, & balanced
\end{cases}
```

Balanced mode is worst case for capacitance.

## 5. Feedback Network

Feedback impedance:

```math
Z_F(s)=R_F \parallel \frac{1}{sC_F}
      =\frac{R_F}{1+sR_FC_F}
```

Ideal closed-loop transimpedance:

```math
Z_T(s)\approx -Z_F(s)
```

Feedback pole:

```math
f_F=\frac{1}{2\pi R_F C_F}
```

Rise time estimate:

```math
t_r\approx\frac{0.35}{f_{3dB}}
```

## 6. Bandwidth Estimate With Op-Amp GBP

For a compensated voltage-feedback op-amp TIA:

```math
f_{3dB,est}\approx
\sqrt{\frac{GBP}{2\pi R_F C_{in,total}}}
```

Required GBP for target bandwidth:

```math
GBP_{min}\approx 2\pi R_F C_{in,total} f_{3dB,target}^2
```

Project bandwidth target:

```math
f_{3dB,target}=10\,\mathrm{MHz}
```

This is only a first estimate. Final validation requires phase margin from AC simulation.

Phase margin check:

```math
PM > 45^\circ \quad \text{minimum}
```

Preferred:

```math
PM \approx 60^\circ
```

## 7. Noise Model

Input-referred rms noise current:

```math
i_{n,TIA,rms}=\frac{v_{n,out,rms}}{R_T}
```

General frequency-domain definition from the PDF:

```math
i_{n,TIA,rms}=
\frac{1}{R_T}
\sqrt{\int_0^{f_u}|Z_T(f)|^2 I_{n,TIA}^2(f)\,df}
```

Important dependency:

```math
I_{n,TIA}(f)=f(C_{in,total},\,R_F,\,opamp,\,switch,\,layout)
```

Larger \(C_{in,total}\) increases high-frequency input-referred noise and reduces bandwidth.

Main noise contributors to include:

| Source | Model |
|---|---|
| Feedback resistor | \(i_{n,R_F}=\sqrt{4kT/R_F}\) |
| Op-amp input current noise | datasheet \(i_n\) |
| Op-amp input voltage noise through input capacitance | grows with \(2\pi f C_{in,total}e_n\) |
| Diode shot noise | \(i_{shot}=\sqrt{2q(I_{ph}+I_D)B}\) |
| APD excess noise | include only if \(M>1\) is modeled |
| Switch leakage noise | only relevant if leakage is comparable to diode dark/signal current |

## 8. Linear Range / Overload

Linear condition:

```math
|I_{in}|R_F < V_{out,lin}
```

Saturation current:

```math
I_{sat,TIA}\approx \frac{V_{out,lin}}{R_F}
```

Optical saturation estimate:

```math
P_{sat,TIA}\approx \frac{I_{sat,TIA}}{R(\lambda)M}
```

For the project requirement:

```math
I_{sat,TIA} > 1\,\mathrm{mA}
```

Working target:

```math
I_{sat,TIA}\ge1\,\mathrm{mA},\quad V_{out,target}=1\,\mathrm{V_{pp}},\quad R_F\approx1\,\mathrm{k\Omega}
```

## 9. Simulation Parameter Sweep

Minimum sweep set:

| Parameter | Sweep |
|---|---|
| \(C_J\) | \(1.0, 1.5, 2.0, 3.0, 5.0\,\mathrm{pF}\) |
| \(R_F\) | from output swing: \(R_F\le V_{out,lin}/1\,\mathrm{mA}\) |
| \(C_F\) | stability sweep around calculated value |
| \(C_{on}\) | switch datasheet min/typ/max |
| \(C_{off}\) | switch datasheet min/typ/max |
| \(R_{on}\) | switch datasheet max at operating bias |
| \(I_{leak}\) | max over temperature |

Measured outputs:

| Output | Criterion |
|---|---|
| DC output | no saturation at \(1\,\mathrm{mA}\) |
| \(Z_T(f)\) | \(-3\,\mathrm{dB}\) bandwidth |
| phase margin | stable with worst-case \(C_{in,total}\) |
| noise | input-referred rms current |
| switch transient | peak glitch and settling time |

## 10. First Design Decision

For \(I_{in,max}=1\,\mathrm{mA}\), choose \(R_F\) from output headroom first.

Then use \(C_{in,total}\) to choose amplifier GBP and \(C_F\).

Do not choose the switch only from logic function. Choose it from:

```text
voltage rating, C_on, C_off, leakage, charge injection/contact bounce, settling time
```
