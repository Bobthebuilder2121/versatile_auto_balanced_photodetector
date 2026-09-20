# Active Requirements

Basis: [April 2026 presentation](../archive/bootstrapping/presentation/PresetationTemplateWide_MPEProject.pdf) (slides 3, 8, 11), [architecture meeting note](../notes/architecture.md), and [selected diode data](diode_parameters.md). The presentation's bootstrap circuit is superseded. Its 1-10 MHz initial target is provisional; slide 3 mentions 100 MHz as a broader ambition. **TBD** means the optical-power range or circuit target is still missing.

## System

| ID | Requirement | Acceptance evidence / open value |
| --- | --- | --- |
| S1 | Select input `I_+`, input `I_-`, or balanced `I_+ - I_-`. | Draw current paths and polarity in all three states. |
| S2 | Externally set and regulate PIN/APD reverse bias. | Verify diode voltage during startup, signal, and mode change; bias tolerance TBD. |
| S3 | Keep the TIA replaceable. | Specify input, reference/bias, supply, output, and control interface; gain/output range TBD. |
| S4 | Select a low-noise input switch. | Compare one relay/RF relay and one analog-switch IC with real datasheets/reference circuits. Check leakage, on/off capacitance, isolation, on-resistance, charge injection, voltage rating, and recovery; limits TBD. |
| S5 | Preserve differential signal and reject common-mode current. | Plot differential transfer and CMRR versus frequency; CMRR target TBD. |
| S6 | Demonstrate system bandwidth. | Initial **1-10 MHz, provisional** (presentation slide 8); measure -3 dB bandwidth per mode with/without switch. |
| S7 | Check maximum signal and switching transients. | No saturation or device-limit violations at specified incident power; power range/recovery limit TBD. |

Zener diodes can protect an input; they are not a linear low-noise selector. Thorlabs PDB570C is a commercial comparison detector, not a bare photodiode.

## Quantities To Determine

| Quantity | Definition / calculation | Current value or missing input |
| --- | --- | --- |
| Wavelength `lambda` | Optical test wavelength. | 1550 nm for the selected pair. |
| Quantum efficiency `eta` | Electrons per incident photon: `eta = R_0*h*c/(q*lambda)`; use APD responsivity at `M=1`. | About 0.76 PIN, 0.64 APD at 1550 nm, from typical responsivity. |
| Responsivity `R(lambda)` | Photocurrent per optical watt, A/W. | PIN 0.95 A/W typ; APD 0.8 A/W typ at `M=1`. |
| Photocurrent `I_photo` | PIN: `R_PIN*P`; APD: `M*R_APD,0*P`. | Incident-power range and APD gain TBD. |
| Junction capacitance `C_J` | Diode capacitance at stated reverse bias. | PIN 1.0 pF typ, 1.5 pF max at 5 V; APD 2.0 pF typ at `0.95*V_BR`. |
| Total input capacitance `C_in` | `C_J + C_amp + C_switch + C_stray`. | Amp, switch, and layout contributions TBD. |
| Shunt resistance `R_sh` | Parallel leakage resistance in diode model. | Not specified for selected pair; do not invent a value. |
| Series resistance `R_s` | Diode ohmic resistance; relevant to high current/fast response. | Not specified; omit initially, revisit if needed. |
| Dark current `I_D` | Current without light at stated bias. | PIN 0.02 nA typ at 5 V; APD 20 nA typ at `0.95*V_BR`. |
| Noise-equivalent power (NEP) | Input-referred noise-current density / effective responsivity, W/sqrt(Hz). | Specify gain, frequency, and noise model; target TBD. |
| Signal-to-noise ratio (SNR) | Signal RMS / integrated noise RMS in stated bandwidth. | Optical power, bandwidth, and noise model TBD. |
| Detectivity `D*` | `sqrt(A)/NEP`, with active area `A`. | Comparable area and NEP data TBD. |
| Detector bandwidth | Bare-diode -3 dB cutoff under datasheet conditions. | PIN 2 GHz typ at 5 V; APD 0.9 GHz typ at `M=10`; both at 50 ohm load. |
| System bandwidth `f_3dB` | Complete signal transfer at -3 dB. | Measure by AC sweep; provisional 1-10 MHz. |
| Rise time `t_r` | 10-90% step rise; `t_r ~= 0.35/f_3dB` for a single-pole response only. | Measure transient response; target TBD. |
| Transimpedance gain `Z_T` | `V_out/I_in`, V/A; low-frequency magnitude about `R_F`. | Set from current range and output swing; target TBD. |
| TIA output `V_out` | `V_ref +/- I_in*R_F` at low frequency; sign depends on polarity. | Output limits and `R_F` TBD. |
| TIA gain-bandwidth product (GBP) | Amplifier unity-gain bandwidth; combine with `R_F`, `C_F`, and `C_in` to check phase margin and -3 dB response. | Select amplifier; verify by AC/loop simulation. Proposed `sqrt(GBP/(4*pi*R_F*(C_F+C_J)))` is not a general bandwidth law. |
| Passive load readout | `V = I_photo*R_L`; `tau = R_L*C_D`. | Applies to a passive resistor load, not the TIA transfer equation. |
| Incident-power limit | Maximum permitted light/electrical reverse current. | PIN 10 mW max at peak wavelength; APD optical max unstated, reverse current max 2 mA. |
| Saturation power `P_sat` | First power where diode or TIA leaves its linear range; TIA estimate `P_sat,TIA ~= (V_available/R_F - I_D)/R_eff`. | The original `V_max/(R(lambda)*Gain)` assumes `Gain=R_F`, negligible offset, and available output swing. Bias/gain/swing TBD. |
| Breakdown voltage `V_BR` | APD reverse voltage at 100 uA dark current. | 50-80 V, 65 V typ; actual operating bias/gain TBD. |

The diode's 50 ohm cutoff is not the complete TIA bandwidth. `C_F` is in the feedback path, so it cannot simply be added to `C_J` as input capacitance. Determine `C_F` and GBP from the selected amplifier and total input capacitance, then verify stability and bandwidth in simulation.

TIA sources: [TI bandwidth design note](https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/transimpedance-amplifiers-what-op-amp-bandwidth-do-i-need-part-i), [TI THS4601EVM guide](https://www.ti.com/lit/pdf/slou150), [Analog Devices stability note](https://www.analog.com/en/resources/technical-articles/stabilize-transimpedance-amplifier-circuit-design.html).
