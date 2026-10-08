# Active Requirements

## System

| ID | Constraint | Metric / target |
| --- | --- | --- |
| S1 | Input modes | Independently switch $I_+\rightarrow\mathrm{OUT}_+$ and $I_-\rightarrow\mathrm{OUT}_-$ according to the truth table below. |
| S2 | External reverse-bias control | PIN: $V_R=5\,\mathrm{V}$ initial test, $V_R<20\,\mathrm{V}$ absolute maximum. APD: $V_R$ set from $M(V_R,T)$ and measured $V_{\mathrm{BR}}$; regulation error $\Delta V_R$: TBD. |
| S3 | Replaceable TIA | Balanced mode has priority. $\lvert Z_T(0)\rvert\ge1\,\mathrm{k\Omega}$; $V_{\mathrm{out,AC,target}}=1\,\mathrm{V_{pp}}$ in balanced mode. For $I_{\Delta,\mathrm{AC,pp}}=200\,\mu\mathrm{A}$, first ideal estimate $R_F=5\,\mathrm{k\Omega}$. Define $V_{\mathrm{ref}}$, supply, output interface and $C_F$. Unbalanced gain is constrained by DC headroom. |
| S4 | Input switching | Compare relay/RF relay and analog-switch IC: $I_{\mathrm{leak}}$, $C_{\mathrm{on/off}}$, $R_{\mathrm{on}}$, $Q_{\mathrm{inj}}$, isolation, voltage rating, $t_{\mathrm{settle}}$; limits: TBD. |
| S5 | Differential/common-mode response | $I_{\mathrm{CM}}=(I_++I_-)/2$; $H_\Delta=V_{\mathrm{out}}/(I_+-I_-)$; $H_{\mathrm{CM}}=V_{\mathrm{out}}/I_{\mathrm{CM}}$; $\mathrm{CMRR}(f)=20\log_{10}\!\bigl(\lvert H_\Delta/H_{\mathrm{CM}}\rvert\bigr)$; target: TBD. |
| S6 | System bandwidth | $\lvert Z_T(f_{3\mathrm{dB}})\rvert=\lvert Z_T(0)\rvert/\sqrt{2}$, per mode, with/without switch; $f_{3\mathrm{dB,target}}=10\,\mathrm{MHz}$. |
| S7 | Linear range and switching transient | $\lvert Z_T(0)\rvert(\lvert I_{\mathrm{in,DC}}\rvert+I_{\mathrm{in,AC,pk}})<V_{\mathrm{headroom}}$ for the low-frequency headroom estimate; check both output limits and diode linearity. Unbalanced: full branch DC; balanced: residual DC mismatch. Peak switch glitch, recovery time and margins: TBD. |
| S8 | Op-amp supply rejection | Prioritize high $\mathrm{PSRR}_+(f)$ and $\mathrm{PSRR}_-(f)$; compare DC minimum/typical values and frequency curves. $\lvert v_{\mathrm{out,PS}}(f)\rvert\approx\lvert NG(f)\rvert\lvert v_{\mathrm{rail}}(f)\rvert10^{-\mathrm{PSRR}(f)/20}$ per rail, with adequate loop gain. Ripple spectrum and output-noise limit: TBD. Photodiode-bias coupling is separate. Prefer manufacturer reference schematics/layouts. |
| S9 | Photocurrent design point | $I_{\mathrm{DC},+}=I_{\mathrm{DC},-}=1\,\mathrm{mA}$ expected per diode; $I_{\mathrm{AC,pp},+}=I_{\mathrm{AC,pp},-}=100\,\mu\mathrm{A}$ design amplitude per diode. DC current is not AC signal amplitude. |

### Input Current Budget

Tutor clarification, 2026-10-06: use $100\,\mu\mathrm{A_{pp}}$ AC per diode; an order-of-magnitude design assumption, not a measured maximum.

$$
I_+(t)=I_{\mathrm{DC},+}+i_{\mathrm{AC}}(t),\qquad
I_-(t)=I_{\mathrm{DC},-}-i_{\mathrm{AC}}(t)
$$

$$
I_\Delta(t)=\underbrace{I_{\mathrm{DC},+}-I_{\mathrm{DC},-}}_{\Delta I_{\mathrm{DC}}}+2i_{\mathrm{AC}}(t)
$$

| Quantity | Single-diode mode | Balanced, equal antiphase AC signals |
| --- | --- | --- |
| DC photocurrent at TIA | $1\,\mathrm{mA}$ | $\Delta I_{\mathrm{DC}}$; ideally zero |
| AC photocurrent, peak-to-peak | $100\,\mu\mathrm{A}$ | $200\,\mu\mathrm{A}$ |
| AC photocurrent, peak | $50\,\mu\mathrm{A}$ for a symmetric waveform | $100\,\mu\mathrm{A}$ for a symmetric waveform |
| Ideal AC output at $R_F=5\,\mathrm{k\Omega}$ | $0.5\,\mathrm{V_{pp}}$ | $1\,\mathrm{V_{pp}}$ |
| Ideal DC output displacement at $R_F=5\,\mathrm{k\Omega}$ | $5\,\mathrm{V}$ magnitude | $5\,\mathrm{k\Omega}\cdot\lvert\Delta I_{\mathrm{DC}}\rvert$ |

Dark-current mismatch and amplifier offsets additionally consume headroom. Supply/output swing and allowable DC mismatch remain TBD. The previous estimate $R_F=1\,\mathrm{k\Omega}$ from $1\,\mathrm{mA}$ and $1\,\mathrm{V_{pp}}$ is superseded: it mixed DC current with AC peak-to-peak amplitude.

### Switching Truth Table

| Mode | $S_+$: $I_+\rightarrow\mathrm{OUT}_+$ | $S_-$: $I_-\rightarrow\mathrm{OUT}_-$ |
| --- | --- | --- |
| $I_+$ | Closed | Open |
| $I_-$ | Open | Closed |
| Autobalanced | Closed | Closed |

$S_+$ and $S_-$ are independent paths into the shared TIA summing node. The diode-current directions produce balanced subtraction; the switches do not subtract the currents.

### Mode Selector

Use a 4-position, non-shorting rotary switch for control logic only. It must not route the photodiode signal current.

| State | $S_+$ | $S_-$ | $\mathrm{AB}_{\mathrm{req}}$ | Function |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | upper diode only; fixed bias reference, PI reset |
| 1 | 0 | 1 | 0 | lower diode only; fixed bias reference, PI reset |
| 2 | 1 | 1 | 0 | balanced, autobalance disabled |
| 3 | 1 | 1 | 1 | balanced, autobalance enabled |

Minimum selector requirement: 3-pole, 4-position, non-shorting. Two poles request the diode reed-relay states; the third requests autobalance, not a third relay coil. Debounce all three requests and sequence SEL1/SEL2 separately; BBM does not eliminate rotary-contact bounce. Raw contacts must not directly drive SEL1/SEL2 or the coil drivers during transitions.

| Lorlin pole | Common, provisional | Contacts connected to request bus | Default |
| --- | --- | --- | --- |
| A | 3.3 V logic | Positions 0, 2, 3 to upper-relay request | 10 kohm pull-down |
| B | 3.3 V logic | Positions 1, 2, 3 to lower-relay request | 10 kohm pull-down |
| C | 3.3 V logic | Position 3 to $\mathrm{AB}_{\mathrm{req}}$; other throws unused | 10 kohm pull-down |

Position numbers are mode labels, not verified physical terminal numbers. Debounce/sequencing implementation and delays: TBD; hold the previous stable mode while contacts settle. After valid switch supplies, disabled/startup state: SEL1=0 (fixed reference), SEL2=1 (reset). Power sequencing must prevent signals outside the TMUX supply limits.

| Part | Type | Fit |
| --- | --- | --- |
| [Lorlin CK1031](https://www.tme.eu/de/details/ck1031/drehschalter/lorlin/) | 3P4T, 4-position, BBM, panel mount, solder lugs, 6 mm shaft | Selected mode-control candidate; TME lists stock |
| Lorlin CK1460 | 3P4T, 4-position, non-shorting, panel rotary | First low-cost candidate |
| Grayhill 51M30-01-3-04S | 3P4T, 4-position, panel rotary | Higher-quality reference candidate |

### Switch Candidates

| Role | Part | Manufacturer | Package | Contact | Shield | Main electrical fit | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Primary | [9002-05-10](https://at.farnell.com/coto-technology/9002-05-10/reed-relay-spst-no-5vdc-0-5a-tht/dp/2981924) | Coto Technology | THT/SIP | SPST-NO, Form A | Coaxial shield | $5\,\mathrm{V}$ coil, $200\,\mathrm{V}$ max, $0.5\,\mathrm{A}$, low guarded capacitance | Candidate for schematic/simulation |
| Secondary | [9012-05-10](https://www.digikey.at/de/products/detail/coto-technology/9012-05-10/418260) | Coto Technology | THT/SIP | SPST-NO, Form A | EMI shield | $5\,\mathrm{V}$ coil, $200\,\mathrm{V}$ max, $0.5\,\mathrm{A}$ | Candidate if coaxial shield is not required |
| Reference | [SIL05-1A72-71L](https://at.farnell.com/c/schutze-schalter-taster-relais/relais/reed-relais?brand=standexmeder) | Standex-Meder | THT/SIL | SPST-NO, Form A | Internal magnetic shield | $5\,\mathrm{V}$ coil, $200\,\mathrm{V}$ max, $0.5\,\mathrm{A}$, $C_{open}\approx0.3\,\mathrm{pF}$ typ | Non-Coto/Pickering comparison only |

Use the coaxial-shielded candidate first for the TIA input node. The Standex part is a reference part, not the first-choice signal switch.

### Relay Coil Variants And Availability

Checked 2026-10-05. Coil voltage is independent of the photodiode reverse-bias voltage. Stock is the displayed distributor inventory, not a delivery guarantee.

| Option | 5 V coil part / stock | 12 V coil part / stock | Coil resistance, 5 V / 12 V | Nominal coil current, 5 V / 12 V |
| --- | --- | --- | --- | --- |
| Coto 9002, coaxial + magnetic shield | [9002-05-10](https://www.digikey.at/en/products/detail/coto-technology/9002-05-10/1914970): 820 | [9002-12-10](https://www.digikey.co.uk/en/products/detail/coto-technology/9002-12-10/1914971): obsolete at DigiKey; no stock shown | $350 / 750\,\Omega$ | $14.3 / 16\,\mathrm{mA}$ |
| Coto 9012, internal magnetic shield | [9012-05-10](https://www.digikey.at/en/products/detail/coto-technology/9012-05-10/418260): 11,653 | [9012-12-10](https://www.digikey.at/en/products/detail/coto-technology/9012-12-10/418262): 7,359 | $500 / 750\,\Omega$ | $10 / 16\,\mathrm{mA}$ |
| Standex SIL, magnetic shield | [SIL05-1A72-71L](https://www.digikey.at/en/products/detail/standex-meder-electronics/SIL05-1A72-71L/2171031): 2,298 | [SIL12-1A72-71L](https://www.digikey.at/en/products/detail/standex-meder-electronics/SIL12-1A72-71L/1949385): 242 | $500 / 1000\,\Omega$ | $10 / 12\,\mathrm{mA}$ |

$I_{\mathrm{coil,nom}}=V_{\mathrm{coil}}/R_{\mathrm{coil}}$. Selected: two Coto 9012-12-10 (12 V), SPST-NO, for $K_+$ and $K_-$. $K_{\mathrm{AB}}$ and the LPF ground clamp are removed. The unity-gain buffer drives $R_{\mathrm{LP}}$ continuously; the LPF stays connected in every mode. Include contact, coil and shield parasitics in each remaining relay model.

| Autobalance state | SEL1, U3A reference selector | SEL2, U3B reset selector | Command source $V_{\mathrm{src}}$ |
| --- | --- | --- | --- |
| Modes 0--2 | 0: S1B to D1 | 1: S2A to D2 (reset) | Fixed $V_{\mathrm{ref},0}$ |
| Mode 3 | 1: S1A to D1 | 0: S2B to D2 (unused throw) | PI output $V_{\mathrm{PI}}$ |

$S_R$ uses U3B to bypass the complete series $R_P$-$C_I$ feedback impedance. With typical $R_{\mathrm{on}}=120\,\Omega$, $\tau_R\approx(R_P+R_{\mathrm{on}})C_I=0.798\,\mathrm{ms}$; DC reset gain is approximately $-R_{\mathrm{on}}/R_{\mathrm{in}}$, not exactly zero. U3B's unused S2B must remain open, not grounded. During U3A's BBM interval, $C_{\mathrm{cmd}}$ retains the command voltage; approximate droop is $|\Delta V_{\mathrm{ref}}|\approx|I_{\mathrm{leak}}+I_{\mathrm{load}}|t_{\mathrm{BBM}}/C_{\mathrm{cmd}}$, excluding charge injection. No reference-hold resistor. The LPF is no longer zeroed in modes 0--2, but the PI is reset and disconnected from the regulator command.

Reset alone is not bumpless transfer: before enabling PI control, its output must match the existing command, including the proportional term. Tracking circuitry is not implemented. On disable, first select the fixed reference (SEL1=0), then reset (SEL2=1). Enable timing, output matching, power sequencing, actuator limits and independent APD bias/current protection remain TBD. This is not a verified protection circuit.

CK1031 requests two separate low-side coil-driver states via control logic. Fit an external flyback clamp per coil; Coto suffix `-10` has no suppression diode, and Standex `71L` is the no-diode variant. Clamp choice affects relay release time. The third Lorlin pole requests autobalance through debounce/sequencing logic.

Selected assembly: 9012-12-10 only for the two diode paths; TMUX6136PWR for the control path. The 9012 parasitic model differs from coaxial 9002; do not reuse it. Standex remains the relay comparison option. Verify package/pinout and shield connections.

Sources: [Coto 9000 datasheet](https://cototechnology.com/library/cotoclassic-9000-series-reed-relay-datasheet.pdf), [Coto 9012 datasheet](https://www.cotorelay.com/datasheets/Classic-9011-9012-9117-Reed-Relay.pdf), [Standex SIL datasheet](https://standexdetect.com/wp-content/uploads/sites/2/2025/09/datasheet-reed-relay-series-sil.pdf).

### Photodiode Bias Bypass

No series bias resistors. Upper bias node: $V_{B+}-U_{\mathrm{trim}}$; lower bias node: $V_{B-}$. Fit $C_b$ from each bias node to quiet analog ground, close to the diode, not across its signal terminal.

$$
C_b=100\,\mathrm{nF}\quad\text{per rail, provisional effective value},\qquad
|Z_C|=\frac{1}{2\pi f C_b}=\begin{cases}1.59\,\Omega,&f=1\,\mathrm{MHz}\\0.159\,\Omega,&f=10\,\mathrm{MHz}\end{cases}
$$

For sinusoidal $I_{\mathrm{AC,pp}}=100\,\mu\mathrm{A}$ per diode, capacitor-only bias ripple at 1 MHz is $V_{\mathrm{bias,pk}}\approx(I_{\mathrm{AC,pp}}/2)|Z_C|=79.6\,\mu\mathrm{V}$ (ideal). This is a sizing estimate, not a ripple requirement or regulator model.

No standalone RC filter or resistive fault-current limit remains. Select voltage rating above the maximum bias-to-ground voltage, including startup/fault transients; verify effective capacitance under DC bias, ESR/ESL, regulator stability and independent APD current protection. Bias voltages and permitted ripple: TBD. Capacitor/regulator interaction: [TI SLVA115A](https://www.ti.com/lit/an/slva115a/slva115a.pdf).

### Command Filter On Our Board

$U_{3A}\rightarrow R_{\mathrm{cmd}}\rightarrow V_{\mathrm{ref}}$, with $C_{\mathrm{cmd}}$ to quiet analog ground. Provisional values: $R_{\mathrm{cmd}}=1\,\mathrm{k\Omega}$, $C_{\mathrm{cmd}}=100\,\mathrm{nF}$. With typical $R_{\mathrm{on}}=120\,\Omega$ at $\pm15\,\mathrm{V}$, $R_{\mathrm{eff}}=1120\,\Omega$ and $f_{c,\mathrm{cmd}}\approx1.421\,\mathrm{kHz}$. Assumptions: high-impedance interface and negligible source impedance. $V_{\mathrm{src}}$ is the selected source before switch resistance; $V_{D1}$ is the actual common-pin voltage.

$$
H_{\mathrm{cmd}}(s)=\frac{V_{\mathrm{ref}}(s)}{V_{\mathrm{src}}(s)}\approx\frac{1}{0.000112s+1},\qquad
H_3(s)=H_0(s)H_{\mathrm{LP}}(s)H_{\mathrm{PI}}(s)H_{\mathrm{cmd}}(s)
\approx\frac{-s-1254.705144}{1.7808\cdot10^{-8}s^3+0.000271s^2+s}
$$

The filter attenuates upstream PI/selector high-frequency noise, not the regulator's own noise. Include resistor/switch thermal noise, voltage-/temperature-dependent $R_{\mathrm{on}}$, leakage, charge injection, capacitance, interface loading and phase lag in validation. Interface levels, supply selection and closed-loop phase margin: TBD. The PI zero near 200 Hz is not a closed-loop bandwidth specification.

### Control Switch Pinout

Selected: [TI TMUX6136PWR, TSSOP-16](https://www.ti.com/lit/ds/symlink/tmux6136.pdf), one IC with two independent SPDT channels. SEL=0 connects B to D; SEL=1 connects A to D. Both symbols depict mode 3: S1 selects A (PI), S2 selects B (unused/open reset branch). In modes 0--2 both selections reverse. S2 disconnects only the reset bypass; the normal $R_P$-$C_I$ feedback path remains connected.

| Signal | Pin | Connection |
| --- | --- | --- |
| S1A / S1B | 2 / 4 | PI output / fixed reference |
| D1 / SEL1 | 3 / 1 | Command-filter input / reference selector control |
| S2A / S2B | 10 / 12 | PI output / leave open (not ground) |
| D2 / SEL2 | 11 / 9 | PI summing node / reset control |
| VDD / VSS / GND | 13 / 5 / 6 | Switch supplies / analog ground |
| N.C. | 7, 8, 14--16 | Leave unconnected |

Decouple each switch rail to analog ground with 100 nF near U3. Supply range: dual $\pm5$ to $\pm16.5\,\mathrm{V}$ or single 10--16.5 V; actual supply TBD. Select logic is provisionally 3.3 V, not 12 V coil wiring. All analog terminals must stay between VSS and VDD, including single-diode-mode output excursions. No connection to the illustrated 150 V gate bias. The switch does not perform level shifting or implement tracking.

## Quantities To Determine

| Quantity | Definition / equation | Selected pair / missing parameter |
| --- | --- | --- |
| Test wavelength | $\lambda$ | $1550\,\mathrm{nm}$. |
| Quantum efficiency | $\eta(\lambda)=R_0(\lambda)hc/(q\lambda)$, using APD $M=1$. | PIN $\approx0.76$; APD $\approx0.64$ (typical). |
| Responsivity | $R_0(\lambda)=I_{\mathrm{ph}}/P_{\mathrm{inc}}$; $R_{\mathrm{APD,eff}}=MR_{\mathrm{APD},0}$. | PIN $0.95\,\mathrm{A/W}$; APD $0.8\,\mathrm{A/W}$ at $M=1$ (typical). |
| APD gain | $M=I_{\mathrm{ph,APD}}/(R_{\mathrm{APD},0}P_{\mathrm{inc}})$. | $M(V_R,T)$: TBD. |
| Photocurrent | $I_{\mathrm{PIN}}=R_{\mathrm{PIN}}P_{\mathrm{inc}}$; $I_{\mathrm{APD}}=MR_{\mathrm{APD},0}P_{\mathrm{inc}}$. | $P_{\mathrm{inc,min/max}}$: TBD. |
| Junction capacitance | $C_J=C_J(V_R)$. | PIN $1.0\,\mathrm{pF}$ typ, $1.5\,\mathrm{pF}$ max at $5\,\mathrm{V}$; APD $2.0\,\mathrm{pF}$ typ at $0.95V_{\mathrm{BR}}$. |
| Total summing-node capacitance | $C_{\mathrm{in}}=C_J+C_{\mathrm{amp}}+C_{\mathrm{sw}}+C_{\mathrm{stray}}$. | $C_{\mathrm{amp}},C_{\mathrm{sw}},C_{\mathrm{stray}}$: TBD; $C_F$ is feedback capacitance. |
| Shunt resistance | $R_{\mathrm{sh}}\approx(\partial I_D/\partial V_R)^{-1}$ at the bias point. | Not specified; measure only if leakage model requires it. |
| Series resistance | $\Delta V=IR_s$. | Not specified; assess at maximum current. |
| Dark current | $I_D=I(V_R,P_{\mathrm{inc}}=0)$. | PIN $0.02\,\mathrm{nA}$ typ at $5\,\mathrm{V}$; APD $20\,\mathrm{nA}$ typ at $0.95V_{\mathrm{BR}}$. |
| Noise-equivalent power | $\mathrm{NEP}(f)=i_{n,\mathrm{in}}(f)/R_{\mathrm{eff}}(\lambda)$, in $\mathrm{W}/\sqrt{\mathrm{Hz}}$. | $i_{n,\mathrm{in}}(f)$, APD excess noise, target: TBD. |
| Signal-to-noise ratio | $\mathrm{SNR}=I_{\mathrm{sig,rms}}/\sqrt{\int_{f_1}^{f_2}i_{n,\mathrm{in}}^2(f)\,df}$. | Signal power and integration band $[f_1,f_2]$: TBD. |
| Specific detectivity | $D^*=\sqrt{A}/\mathrm{NEP}$, $A$ in $\mathrm{cm}^2$. | Active area and NEP at stated conditions: TBD. |
| Bare-diode bandwidth | $f_{3\mathrm{dB,diode}}$ under datasheet load/bias. | PIN $2\,\mathrm{GHz}$ typ at $5\,\mathrm{V}$; APD $0.9\,\mathrm{GHz}$ typ at $M=10$; both $R_L=50\,\Omega$. |
| System bandwidth | $\lvert Z_T(f_{3\mathrm{dB}})\rvert=\lvert Z_T(0)\rvert/\sqrt{2}$. | Target $f_{3\mathrm{dB}}=10\,\mathrm{MHz}$ per mode, with/without switch. |
| Rise time | $t_{10-90}\approx0.35/f_{3\mathrm{dB}}$ for a single-pole response. | Measure per mode; target: TBD. |
| Transimpedance | $Z_T(s)=V_{\mathrm{out}}(s)/I_{\mathrm{in}}(s)$; ideal TIA: $Z_T(s)=-R_F/(1+sR_FC_F)$. | $R_F,C_F$: TBD. |
| TIA output | $V_{\mathrm{out,DC}}\approx V_{\mathrm{ref}}-R_F I_{\mathrm{in,DC}}$; $V_{\mathrm{out,AC,pp}}\approx R_F I_{\mathrm{in,AC,pp}}$ in the flat passband. | Balanced: $200\,\mu\mathrm{A_{pp}}\rightarrow1\,\mathrm{V_{pp}}$ at $R_F=5\,\mathrm{k\Omega}$. Single diode: $1\,\mathrm{mA}$ DC plus $100\,\mu\mathrm{A_{pp}}$ AC; verify clipping. |
| GBP / compensated-TIA estimate | $f_{\mathrm{BW,est}}\approx\sqrt{\mathrm{GBP}/[2\pi R_F(C_{\mathrm{in}}+C_F)]}$; verify actual $f_{3\mathrm{dB}}$ and phase margin. | Amplifier GBP, $C_F$, phase-margin target: TBD. |
| Passive-load comparison | $V=I_{\mathrm{ph}}R_L$; $\tau=R_LC_J$. | Applies to a resistor load, not the TIA transfer function. |
| Incident-power limit | $P_{\mathrm{inc,max}}$ and $I_{R,\mathrm{max}}$. | PIN $10\,\mathrm{mW}$ absolute max at peak wavelength; APD optical limit unspecified, reverse current $2\,\mathrm{mA}$ absolute max. |
| Saturation power | Single diode, DC only: $P_{\mathrm{sat,TIA}}\approx(V_{\mathrm{headroom}}/R_F-I_D)/R_{\mathrm{eff}}$. Balanced: apply the S7 headroom constraint to differential current; check each diode's optical/current limits separately. | $V_{\mathrm{headroom}}$, allowable DC mismatch and diode linearity limit: TBD. Reserve output swing for AC. |
| APD breakdown voltage | $V_{\mathrm{BR}}$ at $I_D=100\,\mu\mathrm{A}$. | $50$-$80\,\mathrm{V}$, $65\,\mathrm{V}$ typ; operating setpoint: TBD. |

Absolute maxima are not operating setpoints. The GBP equation is a compensated, single-pole estimate, not a general bandwidth law.

Sources: [selected diode data](diode_parameters.md); [architecture](../notes/architecture.md); [provisional bandwidth target, slide 8](../archive/bootstrapping/presentation/PresetationTemplateWide_MPEProject.pdf); [TI TIA equations](https://www.ti.com/lit/pdf/slou150).
