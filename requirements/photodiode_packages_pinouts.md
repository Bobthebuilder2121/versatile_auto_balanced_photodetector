# Photodiode Packages And Pinouts

Source: `photodiodes_list.ods`, Sheet1, rows 2-67 (66 entries). Checked: 2026-10-06.

`A` = anode; `K` = cathode; `C` = case; `NC` = not connected. Dimensions in mm.
Groups describe terminal assignment and geometry, not equivalent optical/electrical performance. PIN/APD substitution requires different bias settings. Manufacturer pin numbers are retained; none are invented.

## Pinout Groups

| Group | Package / terminal geometry | A | K | Other terminals | Drawing / view |
|---|---|---|---|---|---|
| H18 | TO-18, 3 pins; pin circle 2.54 | 3 | 1 | 2 = C | [H1], p.4; [H2], p.3; lead-end view |
| T46 | TO-46, ball lens; pin circle 2.5 | 3 | 1 | 2 = C | [T1], p.3; lead-end view |
| T18 | TO-18, flat window; pin circle 2.5 | 1 | 2 | 3 = C | [T3], p.3; lead-end view |
| EB | TO-18 ball lens, 3 pins; asymmetric layout | 3 | 2 | 1 = C/GND | [E1], Fig.6; [E5], Fig.3; lead-end view |
| EG | TO-18 flat window, 2 pins; spacing 1.27 | 1 | 2 | No case pin | [E1], Fig.7; optical/front view: A near tab |
| EA | TO-18 APD, 2 pins; spacing 1.27 | 2 | 1 | No case pin | [E2], Figs.5/7; lead-end view: A near tab |
| E19 | TO-18 PIN, 2 pins; spacing 1.27 | Unnumbered, near tab | Unnumbered, away from tab | No case pin | [E4], Fig.1; optical/front and side views |
| E37 | TO-18 APD, 3 pins; A/K spacing 1.27; offset ground pin | 2 | 1 | 3 = GND | [E3], Fig.9; lead-end view |
| H5 | TO-5, 3 pins; pin circle 5.08 | 1 | 2 | 3 = C | [H3], p.4; lead-end view |
| T5 | TO-5, 3 pins; pin circle 5.1 | 1 | 3 | 2 = C/GND | [T4], p.3; lead-end view |
| EF | TO-5, 3 pins; pin circle 5.08 | Top lead | Right lead | Bottom lead = C/GND | [E6], Fig.2; [E7], Fig.2; lead-end view, tab upper-left |
| E84 | Low-profile TO-5, 3 pins; pin circle 5.08 | Top lead | Left lead | Bottom lead = C | [E8], Fig.7; view not explicitly labelled, tab upper-right |
| EC | Open ceramic carrier, 4 x 2 x 2.03; terminal spacing 2.54 | Right terminal | Left terminal | None | [E1], Fig.5; [E2], Fig.8; optical/top view, as drawn |
| EL-PIN | Ceramic SMD, 3 x 3, 6 pads | 5 | 1, 2, 3, 4, 6 | None | [E9], Fig.1, VS-438R1; underside view |
| EL-APD | Ceramic SMD, 3 x 3, 6 pads | 5 | 1, 2, 3, 4, 6 | None | [E2], Fig.9; underside view; different pad geometry from EL-PIN |
| EL-Si | Top-looking ceramic LCC, 3 x 3, 6 pads | 1, 2, 3, 4, 6 | 5 | None | [E3], Fig.10, VS-337R3; underside view |
| H83 | Plastic SMD, 4 leads; body approx. 4 x 4.7 | 3 | 2, 4 | 1 = NC | [H4], p.5; optical/top view |
| H84 | Plastic lens package, 2 THT leads; spacing 2.54 | Right lead | Left lead | None | [H4], p.6; optical/front view |
| H62 | Glass-epoxy leadless SMD, 5.7 x 4.0 | Right terminal | Left terminal, indexed side | None | [H4], p.6; underside view, as drawn |
| H133 | Ceramic SMD, 4.5 x 3.0, 6 pads | Right middle pad | Left middle pad | Four corner pads = NC | [H5], p.3; underside view, index lower-left |
| EF-FC | FC receptacle, 3 leads | A-labelled lead | K-labelled lead | C-labelled lead | [E1], Fig.8, VS-320; rear view; no pin numbers |
| EF-SC | SC receptacle, 3 leads | A-labelled lead | K-labelled lead | C-labelled lead | [E1], Fig.9, VS-321; rear view; no pin numbers |
| EF-PIG | Fiber-pigtail assembly, 3 leads | Upper lead | Middle lead | Lower lead = C | [E1], Fig.10, VS-322; electrical-end view, as drawn |
| AF-FC | TO-46 inside FC receptacle; pin circle approx. 2.54 | 3 | 1 | 2 = C | [A1], [A3], p.3; [T2], p.3 (explicit bottom view) |
| AF-Si | Fiber-pigtail assembly, 3 leads | 3 | 1 | 2 = C | [A2], p.3; electrical-end view |
| AF-In | Fiber-pigtail assembly, 3 leads | Not explicitly defined | Not explicitly defined | 1 = PD+; 2 = PD-; 3 = C | [A4], p.3; PD+/PD- polarity and view need confirmation |
| TEC | Flanged TO-66, 12 pins | 2 | 12 | 4/5 = thermistor; 6 = C/GND; 7 = cooler-; 9 = cooler+; 1/3/8/10/11 = NC | [E4], Fig.6; electrical-end view, pin marker shown |

**Orientation:** optical/front view looks at the light entrance; lead-end/bottom view looks at the electrical terminals. Mirror the view when constructing a PCB footprint. For drawings without a stated viewing direction, obtain the manufacturer's controlled package drawing before layout.

## TO Packages

| ODS row | Manufacturer | Part number | Type | Group | Package detail |
|---|---|---|---|---|---|
| 2 | Hamamatsu | S5971 | PIN | H18 | Flat window |
| 3 | Hamamatsu | S5972 | PIN | H18 | Flat window |
| 4 | Hamamatsu | S5973 | PIN | H18 | Flat window |
| 5 | Hamamatsu | S5973-01 | PIN | H18 | Mini-lens; same A/K/C layout |
| 6 | Hamamatsu | S5973-02 | PIN | H18 | Flat window |
| 7 | Hamamatsu | S9055 | PIN | H18 | Flat window |
| 8 | Hamamatsu | S9055-01 | PIN | H18 | Flat window |
| 61 | Thorlabs | FGA01 | PIN | T46 | Ball lens; 0.5-diameter leads |
| 63 | Thorlabs | FGA015 | PIN | T18 | Flat window; 0.43-diameter leads |
| 42 | Excelitas | C30617BH | PIN | EB | Ball lens |
| 17 | Excelitas | C30902BH | APD | EB | Ball lens |
| 48 | Excelitas | C30617GH | PIN | EG | Flat window |
| 50 | Excelitas | C30618GH | PIN | EG | Flat window |
| 32 | Excelitas | C30645EH | APD | EA | Small aperture, silicon window |
| 33 | Excelitas | C30645EH-1 | APD | EA | Large aperture, glass window |
| 36 | Excelitas | C30662EH | APD | EA | Large aperture, glass window |
| 37 | Excelitas | C30662EH-1 | APD | EA | Large aperture, glass window |
| 40 | Excelitas | C30662EH-3 | APD | EA | Small aperture, glass window |
| 53 | Excelitas | C30619GH | PIN | E19 | Flat window |
| 54 | Excelitas | C30619GH-LC | PIN | E19 | Low-capacitance option; family outline |
| 25 | Excelitas | C30737EH-230-92 | APD | E37 | 905 nm filter |
| 29 | Excelitas | C30737EH-500-92 | APD | E37 | 905 nm filter |
| 10 | Hamamatsu | S3399 | PIN | H5 | TO-5 |
| 11 | Hamamatsu | S3883 | PIN | H5 | TO-5 |
| 60 | Thorlabs | FDS010 | PIN | T5 | TO-5 |
| 58 | Excelitas | FND-100GH | PIN | EF | TO-5, glass window |
| 59 | Excelitas | FND-100QH | PIN | EF | TO-5, quartz window; older drawing |
| 16 | Excelitas | C30884EH | APD | E84 | Low-profile TO-5; drawing orientation needs confirmation |

## Ceramic And SMD Packages

| ODS row | Manufacturer | Part number | Type | Group | Package detail |
|---|---|---|---|---|---|
| 46 | Excelitas | C30617ECERH | PIN | EC | Open ceramic carrier |
| 51 | Excelitas | C30618ECERH | PIN | EC | Open ceramic carrier |
| 34 | Excelitas | C30645ECERH | APD | EC | Open ceramic carrier |
| 38 | Excelitas | C30662ECERH | APD | EC | Open ceramic carrier |
| 39 | Excelitas | C30662ECERH-1 | APD | EC | Open ceramic carrier |
| 47 | Excelitas | C30617L-100 | PIN | EL-PIN | 6-pad ceramic SMD |
| 52 | Excelitas | C30618L-350 | PIN | EL-PIN | 6-pad ceramic SMD |
| 22 | Excelitas | C30737LH-230-81 | APD | EL-Si | 635 nm filter |
| 23 | Excelitas | C30737LH-230-83 | APD | EL-Si | 650 nm filter |
| 24 | Excelitas | C30737LH-230-92 | APD | EL-Si | 905 nm filter |
| 26 | Excelitas | C30737LH-500-81 | APD | EL-Si | 635 nm filter |
| 27 | Excelitas | C30737LH-500-83 | APD | EL-Si | 650 nm filter |
| 28 | Excelitas | C30737LH-500-92 | APD | EL-Si | 905 nm filter |
| 12 | Hamamatsu | S10783 | PIN | H83 | 4-lead plastic SMD |
| 14 | Hamamatsu | S11062-35GT | PIN | H62 | 2-terminal leadless SMD |
| 15 | Hamamatsu | S13337-01 | PIN | H133 | 6-pad ceramic SMD |

## Lens, Fiber And Cooled Assemblies

| ODS row | Manufacturer | Part number | Type | Group | Package detail |
|---|---|---|---|---|---|
| 13 | Hamamatsu | S10784 | PIN | H84 | 2-lead THT plastic lens package |
| 43 | Excelitas | C30617BFCH | PIN | EF-FC | FC receptacle |
| 49 | Excelitas | C30618BFCH | PIN | EF-FC | FC receptacle; family outline |
| 44 | Excelitas | C30617BSCH | PIN | EF-SC | SC receptacle; different mount from FC |
| 62 | Thorlabs | FGA01FC | PIN | AF-FC | FC/PC receptacle, 3 pins |
| 64 | AeroDIODE | Si-PD-1-A | PIN | AF-FC | FC receptacle, 3 pins |
| 66 | AeroDIODE | InGaAs-PD-1-A | PIN | AF-FC | FC receptacle, 3 pins |
| 65 | AeroDIODE | Si-PD-2-A | PIN | AF-Si | Fiber pigtail with FC/APC |
| 55 | Excelitas | C30619GH-TC | PIN | TEC | Single-stage cooler |
| 56 | Excelitas | C30619GH-DTC | PIN | TEC | Two-stage cooler; different package height |

## Incomplete Or Unverified Entries

| ODS row | Manufacturer | Entry as listed | Package / pinout finding | Missing confirmation |
|---|---|---|---|---|
| 9 | PD-LD / Ushio | PDINBJ070 | Family, not full PN. Type-A drawing: PD+ = A; PD- = K; third lead is ground/reference. [P1], p.2 | Full fiber/connector/bracket/orientation suffix; lead numbering and footprint dimensions |
| 18 | Excelitas | C30737XX-230-80 | XX selects package: PH, CH, LH, MH or EH. [E3] | Replace XX; no unique footprint or A/K assignment |
| 19 | Excelitas | C30737XX-230-90 | Same package-dependent family. [E3] | Replace XX |
| 20 | Excelitas | C30737XX-500-80 | Same package-dependent family. [E3] | Replace XX |
| 21 | Excelitas | C30737XX-500-90 | Same package-dependent family. [E3] | Replace XX |
| 30 | Excelitas | C30644EH | TO-18 APD, confirmed in [E10], p.10 | Exact pinout/outline not verified; not assigned to EA |
| 31 | Excelitas | C30644ECERH | Ceramic-carrier APD, confirmed in [E10], p.10 | Exact terminal drawing not verified; not assigned to EC |
| 35 | Excelitas | C30645L | Legacy SMD designation. Current C30645L-080: EL-APD. [E2], Table 5/Fig.9 | Confirm exact orderable PN and package revision |
| 41 | Excelitas | C30662L | Legacy SMD designation. Current C30662L-200: EL-APD. [E2], Table 5/Fig.9 | Confirm exact orderable PN and package revision |
| 45 | Excelitas | C30617BQC-04-XX | Fiber-pigtail family: EF-PIG. XX is connector selection. [E1], Table 2/Fig.10 | Full connector suffix and controlled outline |
| 57 | Excelitas | C30641EH-TC | Older catalogue: flanged TO-8, TE-cooled. [E11], p.12 | Exact 12-pin assignment not verified for EH-TC; do not substitute the current GH-TC drawing |
| 67 | AeroDIODE | InGaAs-PD-2-A | Fiber pigtail, FC/APC; AF-In labels: 1 = PD+, 2 = PD-, 3 = C. [A4], p.3 | Manufacturer confirmation of PD+/PD- as A/K; do not infer polarity from '+'/'-' alone |

Manufacturer spelling and spaces in `S5973 -02` were normalized; the ODS was not modified.

## Same-Pinning Sets

| Set | Same terminal assignment | Footprint constraint |
|---|---|---|
| H18 | S5971, S5972, S5973, S5973-01, S5973-02, S9055, S9055-01: A3/K1/C2 | Common lead layout; optical height/window differs |
| H5 | S3399, S3883: A1/K2/C3 | Common TO-5 lead layout |
| EB | C30617BH, C30902BH: A3/K2/C1 | Common asymmetric ball-lens lead layout; PIN/APD bias differs |
| EG | C30617GH, C30618GH: A1/K2 | Common 1.27 spacing |
| EA | C30645EH, C30645EH-1, C30662EH, C30662EH-1, C30662EH-3: A2/K1 | Common 1.27 spacing |
| EC | C30617ECERH, C30618ECERH, C30645ECERH, C30662ECERH, C30662ECERH-1: K left/A right | Same nominal carrier geometry; require supplier drawing for production footprint |
| EL-PIN | C30617L-100, C30618L-350: A5/K1,2,3,4,6 | Same SMD drawing |
| EL-Si | All six C30737LH entries: K5/A1,2,3,4,6 | Same SMD drawing |
| AF-FC | FGA01FC, Si-PD-1-A, InGaAs-PD-1-A: A3/K1/C2 | Same mapping; confirm mounting and pin-position tolerances across suppliers |
| TEC | C30619GH-TC, C30619GH-DTC: A2/K12 | Same 12-pin mapping; cooling supply and height differ |

**Do not merge:**
- H18/T46 and T18: both use similar pin circles, but numbers and terminal positions differ relative to the tab.
- EG and EA: physically A near tab/K away from tab, but manufacturer pin numbers are reversed. Use net-labelled pads, not copied symbol pin numbers.
- EL-PIN and EL-APD: same polarity mapping, different pad geometry. EL-Si additionally reverses polarity and uses another pad layout.
- AF-Si and AF-In: different case pin; AF-In A/K polarity not explicitly defined.
- H5, T5, EF and E84: TO-5 designation does not establish common A/K/case placement.

## Datasheet References

All references are manufacturer documents; E7 is a manufacturer PDF hosted by a distributor. Page numbers refer to the PDF page.

[H1]: https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/s5971_etc_kpin1025e.pdf "Hamamatsu S5971/S5972/S5973; outlines p.4"
[H2]: https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/s9055_series_kpin1065e.pdf "Hamamatsu S9055; outline p.3"
[H3]: https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/s3071_etc_kpin1044e.pdf "Hamamatsu S3399/S3883; outlines p.4"
[H4]: https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/s10783_etc_kpin1079e.pdf "Hamamatsu S10783/S10784/S11062-35GT; outlines pp.5-6"
[H5]: https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/s13337-01_kpin1095e.pdf "Hamamatsu S13337-01; outline p.3"
[E1]: https://www.excelitas.com/assets/product/document/excelitas-c30617-and-c30618-series-datasheet.pdf?file=24425.pdf "Excelitas C30617/C30618, Rev.2016.11.08; Figs.5-10"
[E2]: https://www.excelitas.com/assets/product/document/c30645-apd-series-datasheet.pdf?file=27873.pdf "Excelitas C30645/C30662, Rev.2025.11; Table 5, Figs.5/7/8/9"
[E3]: https://prod.excelitas.com/sites/default/files/assets/product/document/24769.pdf "Excelitas C30737, Rev.2017-10; Figs.9-10"
[E4]: https://www.excelitas.com/assets/product/document/excelitas--c30641-series-datasheet.pdf?file=24963.pdf "Excelitas C30619/C30641 family, Rev.2023-01; Figs.1/6"
[E5]: https://www.excelitas.com/assets/product/document/excelitas-c30902-series-family-datasheet.pdf?file=24603.pdf "Excelitas C30902 family, Rev.2022.01; Fig.3"
[E6]: https://www.excelitas.com/assets/product/document/excelitas-fnd-100-series-datasheet.pdf?file=24710.pdf "Excelitas FND-100GH, Rev.2025-02; Fig.2"
[E7]: https://www.htds.fr/wp-content/uploads/2022/12/Excelitas_FND-100_Series_datasheet.pdf "Excelitas FND-100 series, Rev.1.4-2018.04.12; FND-100QH Fig.2"
[E8]: https://www.excelitas.com/assets/product/document/excelitas-c30884eh-si-apd-datasheet.pdf?file=24491.pdf "Excelitas C30884EH, Rev.1.1-2016.08.10; Fig.7"
[E9]: https://www.excelitas.com/sites/default/files/assets/product/document/26041.pdf "Excelitas C30617L-100/C30618L-350, Rev.2021-01a; Fig.1"
[E10]: https://www.excelitas.com/assets/productcategory/document/sensor-solutions-for-defense-aerospace-and-security-applications-catalog.pdf?file=104963.pdf "Excelitas Defense/Aerospace/Security catalogue; C30644 package table p.10"
[E11]: https://prod.excelitas.com/sites/default/files/assets/productcategory/document/104964.pdf "Excelitas Photon Detection catalogue; C30641EH-TC package table p.12"
[T1]: https://media.thorlabs.com/globalassets/items/f/fg/fga/fga01/ttn019860-s01.pdf "Thorlabs FGA01, TTN019860-S01 Rev C; drawing p.3"
[T2]: https://media.thorlabs.com/globalassets/items/f/fg/fga/fga01fc/24112-s01.pdf "Thorlabs FGA01FC, 24112-S01 Rev F; drawing p.3"
[T3]: https://media.thorlabs.com/globalassets/items/f/fg/fga/fga015/ttn125898-s01.pdf "Thorlabs FGA015, TTN125898-S01 Rev B; drawing p.3"
[T4]: https://media.thorlabs.com/globalassets/items/f/fd/fds/fds010/0636-s01.pdf "Thorlabs FDS010, 0636-S01 Rev I; drawing p.3"
[A1]: https://www.aerodiode.com/wp-content/uploads/2025/11/Silicon-Photodiode-Datasheet-Model-1.pdf "AeroDIODE Si-PD-1-A, PN_A402 Rev 02/26; pin configuration p.3"
[A2]: https://www.aerodiode.com/wp-content/uploads/2025/11/Silicon-Photodiode-Datasheet-Model-2.pdf "AeroDIODE Si-PD-2-A, PN_A403 Rev 02/26; pin configuration p.3"
[A3]: https://www.aerodiode.com/wp-content/uploads/2025/11/InGaAs-Photodiode-Datasheet-Model-1-1.pdf "AeroDIODE InGaAs-PD-1-A, PN_A343 Rev 02/26; pin configuration p.3"
[A4]: https://www.aerodiode.com/wp-content/uploads/2025/11/InGaAs-Photodiode-Datasheet-Model-2-1.pdf "AeroDIODE InGaAs-PD-2-A, PN_A399 Rev 02/26; pin configuration p.3"
[P1]: https://www.ushio.com/files/specifications/pd-ld-ingaas-analog-photodiodes-1310-1550.pdf "PD-LD PDINBJ070 family, Analog PIN BJ Rev2; Type-A drawing p.2"
