# Diode Parameter Table

This table extracts the first useful simulation parameters from the local-only diode datasheets in `../literature/Diode_Datasheets/`.

| Device | Type | Material | Wavelength range / peak | Responsivity | Capacitance | Dark current | Bandwidth / rise time | Breakdown / max reverse voltage | Suggested simulation bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hamamatsu G14942-32 | PIN | InGaAs | 0.9-1.7 um / 1.55 um peak | 0.8 min, 0.95 typ A/W at 1.55 um, VR=5 V | 1 typ, 1.5 max pF at VR=5 V, 1 MHz | 0.02 typ, 0.4 max nA at VR=5 V | 2 GHz typ, -3 dB, RL=50 Ohm | 20 V max reverse voltage | Start with VR=5 V |
| Hamamatsu G9801-22 | PIN | InGaAs | 0.9-1.7 um / 1.55 um peak | 0.75 min, 0.9 typ A/W at 1.3 um; 0.8 min, 0.95 typ A/W at 1.55 um | 1 typ, 1.5 max pF at VR=5 V, 1 MHz | 0.02 typ, 0.4 max nA at VR=5 V | 2 GHz typ, -3 dB, RL=50 Ohm | 20 V max reverse voltage | Start with VR=5 V |
| Roithner FCPD-55-C9 | PIN | InGaAs | 0.85-1.7 um | 0.80 min, 0.85 typ A/W at 1301 nm; 0.85 min, 0.90 typ A/W at 1550 nm | 0.5 min, 1.0 typ pF at UR=5 V | 0.2 min, 0.5 typ nA at UR=5 V | 3 GHz min, -3 dB; 0.3 ns max rise/fall time | 45 V min breakdown; 15 V max reverse voltage | Start with UR=5 V |
| Hamamatsu G14858-0020AA | APD | InGaAs | 0.95-1.7 um / 1.55 um peak | 0.65 min, 0.8 typ A/W at 1.55 um, M=1 | 2.0 typ pF at VR=VBR x 0.95, 1 MHz | 20 typ, 50 max nA at VR=VBR x 0.95 | 0.9 GHz typ, M=10, RL=50 Ohm | VBR 50 min, 65 typ, 80 max V at ID=100 uA | Start near VBR x 0.95 only for APD-specific bias tests |

## Selected APD/PIN Pair

Use **G14858-0020AA (APD)** and **G14942-32 (PIN)** as the first concrete comparison at 1550 nm. Both are InGaAs devices with a 1550 nm sensitivity peak; the G14942-32 is also specified for optical measurement/LiDAR. G9801-22 has essentially the same listed electrical PIN values, so it remains a valid alternative. FCPD-55-C9 has lower specified capacitance and a different fiber assembly.

| Characteristic | G14858-0020AA APD | G14942-32 PIN | Consequence for the shared front end |
| --- | --- | --- | --- |
| Spectral range / peak | 950-1700 / 1550 nm | 900-1700 / 1550 nm | Same 1550 nm source can be used. |
| Responsivity at 1550 nm | 0.8 A/W typ at M=1 | 0.95 A/W typ | APD signal is `0.8*M*P` A; PIN signal is `0.95*P` A, with `P` in W. |
| Terminal capacitance | 2.0 pF typ at `VR=0.95*VBR` | 1.0 pF typ, 1.5 pF max at 5 V | Test at least 1.0, 1.5 and 2.0 pF; include switch and TIA input capacitance separately. |
| Dark current | 20 nA typ, 50 nA max at `VR=0.95*VBR` | 0.02 nA typ, 0.4 nA max at 5 V | APD DC offset and current noise require a separate check. |
| Specified -3 dB cutoff | 0.9 GHz typ at M=10, 50 ohm load | 2 GHz typ at 5 V, 50 ohm load | These are detector test conditions, not the bandwidth of the eventual TIA. |
| Reverse bias | `VBR=50-80 V`, 65 V typ; `0.95*VBR` is about 61.75 V for a typical device | 5 V datasheet test condition; 20 V absolute maximum | Bias supply and switch ratings must cover distinct APD and PIN modes. APD bias must be set using the actual device's breakdown/gain data. |
| Optical interface | TO-18 window, 0.2 mm active diameter | FC/APC receptacle | The electrical comparison is valid, but a physical swap needs different optical coupling. |

**First controlled comparison:** use the same wavelength (1550 nm), power incident on each diode, TIA and switching path in both modes. Model each diode as a photocurrent source in parallel with its capacitance; set the PIN at 5 V and the APD at a specified gain/bias operating point. For example, at 1 uW incident power and `M=10`, typical signal current is 0.95 uA for the PIN and 8 uA for the APD. The APD's `M=10` is an explicit comparison setting, not a claim that `VR=0.95*VBR` always produces this gain. Measure gain, -3 dB bandwidth and DC output shift in each mode. Then repeat with *equal injected current* to isolate the effect of capacitance and bias from avalanche gain. A later noise comparison needs an APD gain/excess-noise model; the current source and capacitor alone cannot predict it.

Sources: local-only PDFs in `../literature/Diode_Datasheets/`; [G14858-0020AA datasheet](https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/g14858-0020aa_kapd1068e.pdf), [G14942-32 product/specifications](https://www.hamamatsu.com/jp/en/product/optical-sensors/infrared-detector/ingaas-photodiode/G14942-32.html), [G9801 series datasheet](https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/g9801_series_kird1081e.pdf), [FCPD-55-C9 datasheet](https://www.roithner-laser.com/datasheets/pd/fcpd-55-c9.pdf).

## Parameter Ranges For Generic Simulation

| Parameter | Useful first range | Brief explanation |
| --- | --- | --- |
| PIN capacitance | 0.5-1.5 pF | Use this as the input capacitance range for generic PIN simulations. |
| APD capacitance | about 2 pF | Use this as the first APD capacitance value; later it can be swept around this point. |
| PIN responsivity near 1550 nm | about 0.85-0.95 A/W | Converts optical power into photocurrent for PIN cases. |
| APD responsivity at M=1 near 1550 nm | about 0.65-0.8 A/W | Base responsivity before avalanche multiplication is applied. |
| PIN dark current at 5 V reverse bias | about 0.02-0.5 nA typical across candidates | Leakage current to include as a DC error/noise-related term; the Hamamatsu PINs specify 0.4 nA maximum. |
| APD dark current near VBR x 0.95 | about 20-50 nA | APD leakage is much higher and matters for biasing and noise. |
| PIN reverse bias for first simulations | 5 V | Common datasheet test condition and a sensible starting bias. |
| APD breakdown voltage range | 50-80 V, 65 V typical | Defines the high-voltage bias region for the APD case. |
| Candidate detector bandwidths | 0.9-3 GHz, well above the planned 1-10 MHz circuit target | The diode itself is probably not the bandwidth bottleneck at first; the TIA/control loop is. |

## How To Use This In The Next Simulation

Use the datasheet values to create two detector cases:

| Case | Model | Suggested values |
| --- | --- | --- |
| G14942-32 PIN | Photocurrent source in parallel with capacitance | Start at 1.0 pF, sweep to its 1.5 pF maximum; use 5 V reverse bias |
| G14858-0020AA APD | Photocurrent source in parallel with capacitance, with APD reverse-bias check | Start at 2.0 pF near `0.95*VBR`; select APD bias for the intended gain |

For photocurrent, use:

```text
I_PIN = R_PIN * P
I_APD = M * R_APD_at_M1 * P
```

If the expected optical power is not fixed yet, sweep current directly instead of pretending that one optical power value is already known.
