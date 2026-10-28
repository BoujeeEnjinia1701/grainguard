---
doc_id: GGD-CAL-001
title: GrainGuard sizing calculations
project: GrainGuard
doc_type: Calculation
version: "0.7"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (bin and airflow, fan heat, moisture error, rewetting in cool mode, coverage, power, radio, cable loads, mast, cost, requirement status)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Plenum probe in the base kit; new check B10 on measured fan heat; R4 from at risk to met; kit $247.00 to $256.50 with the $6.50 overrun accepted (R13)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($250 to $260, GGD-DDR-002); script rerun; R13 not met, overrun accepted, to met
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design for construction (GGD-DDR-003). Radio uses the modelled antenna height; mast check uses the modelled panel and shield heights; new checks F5 (stay) and F6 (mast with the stay off); cable and conduit lengths; cost reported against the value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: R8 row, section D and section G note the 2026-10-02 decisions (GGD-DEC-001, items 2 and 6); no number changed
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: Follow-ups to the 2026-10-02 decisions carried out. 20 W panel in the model and BOM; section D and the mast check (F4 to F6) rerun for it; R8 not met to met; stay-off check no longer holds at 45 m/s, so a 30 m/s service limit is proposed; adjustable disconnect (D4); kit USD 389.50 to USD 406.50
- version: "0.7"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.8 upgrade and STEM check GGD-STM-001: mast tube checked at the 195 MPa of S195T (D12); stay-off service rule decided under the standing instruction (D12, closes open item 9); battery freezing against the disconnect setting (G3, R9 not met, fix proposed to Amish); battery hydrogen vents (G4, D10); winter shading and the mast siting rule (G5, D13); cost USD 410.50; requirements now GGD-PRS-001"
---

# GrainGuard sizing calculations

On paper, GrainGuard meets seven of its fourteen requirements (eight of fifteen in GGD-PRS-001, which adds the retrofit requirement PR-015), has two at risk, has two that cannot be verified at TRL 3 and has two **not met**, each with a fix proposed to Amish: with the low-voltage disconnect at the 50 % figure decided on 2026-10-02, the battery's electrolyte freezes near -20 °C, above the -30 °C of R9 (section G); and once a lead-acid charge efficiency of 85 % is included, the 20 W panel refills the battery from half charge in 3.5 winter days, not the 3 of R8 (section D; version 0.6 gave 2.9 days without it). Cost (R13) is reported against a value-engineering target. With the relay input specified at 3 mA the battery lasts 7.7 days with no sun. The price is a larger load on the mast: with the stay off, the mast alone does not meet the 1.5 times margin at a 45 m/s gust, so the stay comes off only in gusts under 30 m/s (section F; decided under Amish's standing instruction of 2026-10-23 after the STEM check found the mast tube is S195T, not S235, GGD-DEC-001 D12). Version 0.7 adds the STEM check's findings and its independent review: the yield of the mast tube, the battery's freezing point against its disconnect setting, the charge efficiency, the battery's hydrogen vents (D10), the rule that the mast stands south of the bin so the bin never shades the panel (D13), the legal radio mode (500 kHz bandwidth, D15), the rope's clipped eye, the welded base in the stay check and the diagonal wind case for the anchors. Version 0.4 followed the design for construction (GGD-DDR-003) and version 0.6 adds the 2026-10-02 decisions: the constructable design costs USD 410.50 per bin against a value-engineering target of USD 260 (USD 150.50 over the target, with the vents of version 0.7), with the farmhouse receiver costed per farm; the radio margin, mast stresses and cable lengths now come from the modelled antenna, bracket and route, and all still meet their requirements. Amish adopted the plenum temperature probe into the base kit on 2026-09-25 (GGD-DDR-002), so the fan's own heat, worth about one point of moisture per degree, is measured and the fan decision (R4) is met. The two at risk are the moisture estimate (R2) and heating detection away from the center (R6). The calculations also corrected three TRL 2 figures: the reference bin holds about 88.8 t, not 95 t, because the aeration floor sits 0.4 m above the pad; the fan heat of "about 1 °C" is right only for a 0.4 kW fan; and the radio margin at 1 km past a building is about 18 dB, not 48 dB. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace the bin maker's roof and hanger ratings, a licensed electrician's design of the starter interface, or a confined-space entry procedure. Nothing may be installed in a bin on the strength of this note. GrainGuard must never be used to judge whether a bin is safe to enter. See GGD-PRC-001, Safety.

## Scope and method

The note checks every requirement in GGD-PRS-001 v0.9 (by its old R number, given in the PRS's "Was" column) against the design in GGD-PRC-001 v1.0, as made constructable in GGD-DDR-003, and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()`, so the bin, pod positions, rope length, cable route and mast dimensions used here are the ones in the STEP files and on drawing GGD-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the requirement table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The reference case is unchanged from TRL 2: a 5.49 m (18 ft) corrugated steel bin with a 5.6 m eave, a full perforated floor and one aeration fan, holding shelled corn at a target of 15.0 % moisture, wet basis, in the US Corn Belt (GGD-DDR-001, D11).

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Bin | Aeration floor 0.4 m above the pad; grain level with the eave, so 5.2 m deep | Model `PARAMS`; typical floor supports |
| Grain | Corn at 721 kg/m³ bulk; specific heat 1.465 + 0.0356 M kJ/(kg·K) with M in % wet basis | Common handbook values |
| Moisture | ASABE D245.6 modified Henderson equation for corn (K 8.6541e-5, N 1.8634, C 49.81) | ASABE standard |
| Airflow | 0.2 cfm/bu; Shedd resistance for corn (ASABE D272, a 2.07e4, b 30.4), packing factor 1.5, 50 Pa for duct and floor | ASABE standard; packing and duct losses assumed |
| Fan | 0.37 kW (1/2 hp) class, 0.40 kW input, motor in the air stream, so all input power heats the air; range 0.2 to 1.1 kW checked | Assumed; fans on real bins vary |
| Sensors | SHT45 ±1.0 % RH and ±0.1 °C typical ([Sensirion](https://sensirion.com/products/catalog/SHT45)); SHT40 ±1.8 % RH typical, ±3.5 % RH maximum ([Sensirion](https://sensirion.com/products/catalog/SHT40)), ±0.2 °C typical ([SHT4x datasheet](https://sensirion.com/resource/datasheet/sht4x)); plenum probe DS18B20 ±0.5 °C from -10 °C to +85 °C ([Analog Devices](https://www.analog.com/en/products/ds18b20.html)) | Datasheets |
| Power | Controller 25 mW; pod bus 0.72 W for 3 s every 10 min; LoRa 0.15 W for 0.37 s every 10 min; charge controller 6 mA; relay input 3 mA at 12 V; 7 Ah AGM, 50 % usable (low-voltage disconnect at about 12.1 V), 60 % of that at -20 °C; 20 W panel; winter 1.5 peak sun hours, 60 % derating | As at TRL 2, except the relay input (was 10 mA) and the panel (was 10 W) |
| Radio | 14 dBm, -132 dBm at SF10 and 125 kHz, 0 dBi antennas, 1 dB cable loss each end; antennas 2.22 m (mast, from the model) and 2.0 m (farmhouse); 20 dB for one farm building; plane-earth path loss | Typical SX1262 figures; building loss assumed |
| Cable loads | Janssen pressures with K 0.5 and wall friction 0.4; grain on steel 0.3; pod drag = vertical pressure on the pod face plus side friction; unloading overpressure factor 2.0 | Screening values, not a bin-load standard |
| Mast | 45 m/s gust (1,215 Pa); drag coefficient 1.2 on the panel (350 x 430 mm) and 1.0 on the shield; mast welded to its base plate and propped by the stay, which is bolted twice at each end; mast tube S195T (EN 10255, 195 MPa), stay angle S235 | Screening values; tube grade from the maker's declaration of performance |

## A. Bin, airflow and fan heat (R4)

- **Grain.** The bin's cross-section is 23.67 m² and the grain is 5.2 m deep [A1], so it holds 123.1 m³, about 3,493 bu or 88.8 t of corn [A2]. The TRL 2 figures of 132 m³ and 95 t took the full 5.6 m eave height as grain depth and are corrected in all documents.
- **Airflow and pressure.** At 0.2 cfm/bu the fan moves 0.330 m³/s (699 cfm), a superficial speed of 13.9 mm/s [A3]. The static pressure is about 139 Pa (0.56 in wc) [A4], so the air power is only 46 W [A5]. Fans on real bins are much larger than this air power suggests; 0.40 kW input is assumed.
- **Fan heat.** With the motor in the air stream, all of the fan's input power warms the air, at 0.415 kW/K [A6]. The rise is 0.5 °C for a 0.2 kW fan, 1.0 °C for 0.4 kW, 1.8 °C for 0.75 kW and 2.7 °C for 1.1 kW [A7]. The TRL 2 figure of "about 1 °C" holds only for the smallest fans.
- **Cooling time.** A cooling front passes through the bin in 75 h by the extension rule to 119 h by a sensible-heat balance [A8]. Cooling the grain by 10 °C removes about 493 kWh; the fan uses about 48 kWh per cycle, about $6 of electricity [A9].

## B. Moisture estimate and the decision rule (R2, R3, R4)

- **The key sensitivity.** Air at 10 °C and 70 % RH has an EMC for corn of 15.70 %; warmed 1.0 °C by the fan it drops to 65.5 % RH and 14.73 %, so each degree of fan heat moves the plenum EMC by about 0.97 points [B1], [B2]. Across fans of 0.2 to 1.1 kW the same outside air gives a plenum EMC from 13.36 % to 15.21 %, a spread of 1.85 points [B3]. That is more than twice the whole moisture tolerance in R2, so an unmeasured fan heat would be the largest error in the decision rule.
- **Plenum probe, now in the base kit.** Heating does not change the air's humidity ratio, so the plenum RH follows from the ambient humidity ratio and the plenum temperature alone. A temperature-only probe in the fan transition (BOM item 14, $9.50) therefore removes the fan heat error without a second RH pod. Amish adopted it into the base kit on 2026-09-25 (GGD-DDR-002). With the DS18B20 at ±0.5 °C and the ambient SHT45 at ±0.1 °C, the measured fan heat is known within ±0.51 °C, so the plenum EMC is known within about ±0.50 points, against the 1.85-point spread when the fan heat is only a setting [B10]. The probe's ±0.5 °C rating applies from -10 °C to +85 °C; below -10 °C its error is larger and not quantified here; checking the probe against the ambient sensor with the fan off is a TRL 4 bench task. The fan heat is measured during each run; the controller uses the last measured rise to decide whether to start the fan. R4 is **met** on paper.
- **Sensor error.** The sensor-induced EMC error at 15 °C and 60 % RH is 0.17 points for the SHT45 and 0.31 points for the SHT40 (typical accuracy). Over 20 % to 75 % RH and 0 to 30 °C, the worst case is 0.23 and 0.42 points, both at 0 °C and 75 % RH. At the SHT40's maximum tolerance of ±3.5 % RH it reaches 0.81 points, just over the 0.8-point target [B5]. At 85 % RH (wet grain) the SHT45 error is still only 0.29 points, but this is where the equation itself is least reliable [B6].
- **What is not included.** Membrane lag, sensor hysteresis and drift, and the fit error of the EMC equation are not in these figures [B7]. The equation's fit error for a given corn lot is not known at TRL 3 and is likely to be of the same order as the target. R2 is therefore **at risk**, not met.
- **Rewetting in cool mode.** The cool-mode allowance lets the fan run with plenum air up to 1.0 point of EMC above target. At an 11.0 °C plenum, air at 66.9 % RH holds corn at 15.0 % and air at 72.1 % RH holds it at 16.0 %; the difference is 0.42 g of water per kilogram of air [B8]. Over one 119 h cooling cycle at the full allowance, that is at most 74 kg of water, enough to raise the bottom 0.37 m of grain (7 % of the depth) by one point [B9]. The reworded pitch ("without rewetting it") is therefore true for hold mode and for cool mode within this bound; see `docs/REVIEW.md`.
- **Ambient air (R3).** The SHT45 meets ±0.3 °C and ±2 % RH on its own, but the radiation error of a passive shield in sun and low wind is not known without a test. R3 is **not verifiable at TRL 3**.

## C. Sensing geometry, coverage and alarm latency (R1, R6)

- **Profile.** Six pods at 0.94 m pitch sit 0.25 m to 4.95 m above the floor, with the top pod 0.25 m below a level grain surface [C1]. With ±0.1 °C (SHT45) and ±0.2 °C (SHT40) typical accuracy, R1 is **met**.
- **Coverage.** A sensor sees a developing hot spot only within about 0.5 m ([Ileleji et al., Purdue](https://engineering.purdue.edu/ABE/people/Papers/klein.ileleji.1/hotspot)). One center cable watches 0.79 m² of the 23.7 m² section, 3.3 % [C2]; covering the whole section at that spacing would take about 31 cables [C3]. The center core, where fines collect under the fill spout, is watched; the outer ring is not.
- **Latency.** With 10 min sampling and up to three LoRa retries a minute apart, an alarm reaches the farmhouse within about 13 min [C4], inside the 15 min target. R6 is **at risk** because of coverage, not latency.

## D. Power (R8, R12)

*Table 2. Daily energy use [D1] to [D3].*

| Load | Wh per day |
| --- | --- |
| Controller and regulators, 25 mW | 0.600 |
| Pod bus, 0.72 W for 3 s every 10 min | 0.086 |
| LoRa transmit, 0.15 W for 0.37 s every 10 min | 0.002 |
| Charge controller self-use, 6 mA | 1.728 |
| Relay input, 3 mA while the fan runs | 0.288 at 8 h; 0.864 continuous |
| **Total, fan 8 h per day / continuous** | **2.70 / 3.28** |

- **Autonomy.** The TRL 2 design had a 10 mA relay input and used 5.30 Wh per day with the fan running continuously [D2]. The 7 Ah AGM battery gives 25.2 Wh usable at -20 °C [D4] with the adjustable low-voltage disconnect set to about 12.1 V (GGD-DEC-001, item 6; the 50 % figure the earlier assumption already used), so it lasted 4.8 days. Raising the disconnect to protect the battery at -30 °C costs autonomy: section G gives 5.4 days at the 65 % figure and 4.6 days at 70 % [G3]. With the relay input specified at 3 mA or less (an optically isolated input, BOM item 11), daily use falls to 3.28 Wh and autonomy rises to 7.7 days with the fan continuous and 9.3 days at 8 h per day [D3], [D5]. The autonomy half of R8 is met with no added cost.
- **Recovery.** Amish decided on 2026-10-02 to fit a 20 W panel (GGD-DEC-001, item 2; BOM line 8, USD 34.00). At 1.5 winter peak sun hours with the 60 % derating (which covers PWM mismatch, heat, dirt and wiring) it yields 18.0 Wh per day; version 0.6 took all of it into the battery and found a refill from half charge in 2.9 days. A lead-acid battery stores about 85 % of the energy put into it, which the independent review found missing: 15.3 Wh reaches the battery, a net 12.0 Wh with the fan continuous, so the refill takes 3.5 days at 1.5 peak sun hours and 1.9 days at 2.5 [D6]. Refilling in 3 days takes about 23 W [D7]. The recovery half of R8 is **not met**; a 25 W panel (2.7 days) is proposed to Amish, because the panel size was his decision (GGD-DEC-001, open item 12). The 1.5 peak sun hours is an assumption, to confirm from NREL data for the host site. Both halves of R8 depend on the mast standing south of the bin: at the winter solstice the noon sun is 24.6 degrees up at 42 °N and the wall's shadow is 12.3 m long, so on the north side the panel would be in shade all day [G5] (GGD-DEC-001 D13).
- **Charging voltage (R12).** A temperature-compensated AGM charger raises its absorption voltage to 15.75 V at -20 °C and 16.05 V at -30 °C, over the 15 V limit in R12. The charge controller is therefore specified with its compensation clamped at 15.0 V [D8]. With that specification R12 is **met**.

## E. Radio (R7)

- **Legal mode.** In the US 902 to 928 MHz band, 47 CFR 15.247 allows a frequency-hopping system (with channels under 250 kHz wide, at least 50 channels and no more than 0.4 s on one channel in 20 s) or a digital modulation system with a 6 dB bandwidth of at least 500 kHz. Version 0.6 planned one fixed 125 kHz channel, which is neither; the independent review found it. The radio now runs at SF10 with a 500 kHz bandwidth on one channel, at both ends, a firmware setting (GGD-DEC-001 D15). Its spectral density at 14 dBm is -8.2 dBm in 3 kHz against the 8 dBm limit [E6].
- **Budget and margin.** At 500 kHz the receiver is about 6 dB less sensitive (-126 dBm against -132 dBm at 125 kHz), so the link budget is 138 dB [E1]. With the antenna on its mast bracket (centre 2.22 m above the pad, GGD-DDR-003), plane-earth loss at 1 km is 107.1 dB, well past the 54 m breakpoint; with 20 dB assumed for one farm building the margin is 10.9 dB (16.9 dB at 125 kHz) [E3]. With a 10 dB fade margin the same model gives about 1.06 km [E4]. R7 is **met** on paper with little to spare; a summer corn crop round antennas 2 m up and the bin itself are not in the model, so the site survey at TRL 4 decides.
- **Airtime.** A 24-byte packet takes 93 ms at SF10 and 500 kHz [E5]; the 0.4 s dwell limit no longer applies, but the payload stays at 24 bytes.

## F. Cable loads and mast (R10)

- **Pull-down force.** Janssen's method gives 25.8 kPa vertical and 12.9 kPa lateral pressure at the floor [F1]. The static drag is 213 N on the rope and 825 N on the six pods, 1,038 N in all, and about 2,076 N with an unloading overpressure factor of 2.0 [F2]. The TRL 2 design force of 2.5 kN is kept, 1.2 times this estimate [F3]. No measurement exists for a 6 mm cable with pods, so the estimate is unverified (STEM check S22). The measured maximum of 4.7 kN on the largest commercial cable ([Illinois Experts, ASABE](https://experts.illinois.edu/en/publications/forces-on-monitoring-cables-during-grain-bin-filling-and-emptying/)) is consistent with a larger cable in a larger bin.
- **Rope.** A 20 kN rope holds about 16 kN at its clipped eye (wire rope clips develop about 80 % of the rope's strength), a factor of 6.4 on 2.5 kN against R10's 4, and 3.4 times the 4.7 kN measured on the largest commercial cable [F3]. The roof hanger rating comes from the bin maker, bin by bin, so R10 as a whole is **not verifiable at TRL 3**.
- **Mast.** At a 45 m/s gust, the 20 W panel (350 x 430 mm, centre 2.24 m up on its bracket) and the shield (1.89 m) put 219 N and 31 N on the mast (the 10 W panel gave 128 N), a moment of 155 N·m at the stay. The DN25 tube (section modulus 2.14 cm³) sees 73 MPa, 2.7 times below the 195 MPa yield of S195T [F4]. Version 0.6 used 235 MPa (3.2 times); 33.7 x 3.2 mm galvanized tube is EN 10255 medium series, whose grade is S195T ([Parker Steel declaration of performance](https://parkersteel.co.uk/webshared/media/pdf/dop/PS-DOP028-S195T-GAS-WATER.pdf), accessed 2026-10-24).
- **Stay.** With the welded base acting as a fixed end, the stay props the mast with about 397 N (348 N if the base were pinned, as version 0.6 took it). It is bolted twice at each end, so wind along the wall bends it as a guided cantilever 592 mm long: 76 MPa in the 40 x 40 x 4 angle, 3.1 times below yield. Toward the wall it is a strut with a buckling load of about 104 kN [F5].
- **Mast with the stay off.** If the stay is removed for service, the welded base carries the mast alone. With the 20 W panel at a 45 m/s gust that is 550 N·m at the base and 257 MPa in the tube, over the 195 MPa yield, so the condition Amish set on 2026-10-02 (the check "still passes") is **not met at 45 m/s**. The 1.5 times margin holds up to a 32 m/s gust; at 30 m/s the tube sees 114 MPa (1.7 times below yield) and, with the wind on the base plate's diagonal, the worst M10 anchor pulls 1.15 kN (2.59 kN at 45 m/s) [F6]; the anchors' rating in the pad's concrete is to confirm with the anchor maker. A DN32 mast would not reach the 1.5 times margin at 45 m/s either (about 140 MPa against 130 MPa). The stay therefore comes off only on a calm day with no strong wind forecast (gusts under 30 m/s, about 65 mph) and is refitted before leaving: decided under Amish's standing instruction of 2026-10-23 as the fix for STEM check row S24, closing open decision 9 (GGD-DEC-001 D12); Amish can reverse it.
- **Lengths.** The rope hangs 6.51 m below its thimble. The bus cable is 16.8 m (main run 10.5 m, five pod jumpers 5.4 m, 0.9 m of ends inside the pods and the box), 7.3 m of it inside the bin; the BOM carries 18.5 m. The conduit is 6.2 m [G1].

## G. Environment (R9)

- **Battery freezing.** Lead-acid electrolyte freezes near -20 °C at 50 % state of charge and below -50 °C when full, by the BCI table for flooded cells; AGM electrolyte is denser and freezes a few degrees lower, to confirm on the chosen battery's datasheet [G2]. Interpolating the table, a disconnect at 50 % lets the electrolyte freeze near -20 °C, at 65 % near -30 °C and at 70 % near -36 °C. The days with no sun and the fan held on are 7.7, 5.4 and 4.6 if the 60 % cold derating of section D applies as well, or 12.8, 9.0 and 7.7 if it does not at the station's very low draw (about C/600, where little capacity is lost to the cold) [G3] ([Trojan, BCI table](https://ressupply.com/documents/trojan_battery/Deep_Cycle_Battery_Storage_Guide.pdf), accessed 2026-10-24). Amish decided on 2026-10-02 (GGD-DEC-001, item 6) on a controller with an adjustable disconnect set to the battery maker's 50 % figure at -20 °C, about 12.1 V; at the -30 °C lower limit of R9 that battery can freeze. The 70 % figure leaves a 6 K margin below -30 °C, and its autonomy is met on the low-draw basis and short on the conservative one; a cold-chamber test at TRL 4 settles which. An empty battery stops the fan, the safe state; a frozen one cracks. Because it changes his decision, the 70 % figure is proposed to Amish (GGD-DEC-001, open item 11) rather than made here. R9 is **not met** until he decides.
- **Battery hydrogen.** A valve-regulated battery charged hard in the cold gives off hydrogen. By the IEC 62485-2 method (Q = 0.05 n Igas C 10⁻³ m³/h with Igas 8 mA/Ah for valve-regulated cells on boost, and an opening of A = 28 Q cm² in and out), the box needs 16.8 L/h of air while charging (2.1 L/h on float), through 0.47 cm² openings low and high [G4] ([INOTEC, EN 50272-2 method](https://www.inotec-licht.de/en/practice/venting-and-aerating-batteries/), accessed 2026-10-24). The single membrane breather of version 0.6 has no open area. Two M16 labyrinth vents with a 10 mm bore, one in the bottom face and one at the top of the side wall, give 0.79 cm² each before the labyrinth's own loss, which the vent maker's data will give (GGD-DEC-001 D10). The box is then IP66 except at its vents, which are IP55 or better, to confirm from the vent maker.
- **Phosphine.** Phosphine resistance of the pods is still unverified (conformal coating, a test board through one fumigation at TRL 4).
- **Winter sun.** See section D: the mast stands south of the bin [G5].

## H. Cost (R13)

`budget_usd` is a hypothetical value-engineering target, not a limit (Amish, 2026-10-01).

- Value-engineering target: USD 260. Estimated cost of the constructable design: USD 410.50 per bin, items 1 to 11 and 13 to 17 (USD 150.50 over the target) [H1].
- The concept kit was USD 256.50 (USD 247.00 after the GGD-DDR-001 trims, plus the USD 9.50 plenum probe [H3]). Making it buildable added USD 133.00, the 2026-10-02 decisions a further USD 17.00 (the 20 W panel, USD 9.00, and an adjustable-disconnect charge controller, USD 8.00; both indicative, no quotes) and the two battery vents of version 0.7 USD 4.00 (an estimate) [H4]: the mast weldment, stay, wall bracket, anchors and six clamps (line 10, now USD 53.00), the pod glands and stops, the enclosure mounting plate, and three lines missing from the concept (antenna, battery fuse and surge protection, conduit). The cost drivers and savings worth trying are in the design decisions register, GGD-DEC-001.
- The farmhouse receiver adds USD 22.00 once per farm; a first prototype with one bin costs USD 432.50 [H2].

## Requirement status

*Table 3. Status of every requirement, by its R number (PR number in GGD-PRS-001) [I1], [I2]. Not met items first.*

| ID | Requirement | Value at TRL 3 | Target | Status |
| --- | --- | --- | --- | --- |
| R9 | Environment | Electrolyte freezes near -20 °C at the 50 % disconnect (65 % proposed, near -30 °C); vents 0.79 cm² each against 0.47 cm²; phosphine unverified | -30 °C to +50 °C; IP66 with IP55 vents; one fumigation | Not met |
| R2 | Moisture estimate | Sensor-only error 0.23 points (SHT45) and 0.42 points (SHT40) worst case; 0.81 at the SHT40 maximum; equation error not included | ±0.8 points, 20 % to 75 % RH | At risk |
| R6 | Heating alert | Center core only, 3.3 % of the section; latency about 13 min | Any pod, alarm within 15 min | At risk |
| R3 | Ambient air | SHT45 ±0.1 °C and ±1.0 % RH; shield error unknown | ±0.3 °C, ±2 % RH | Not verifiable at TRL 3 |
| R10 | Mechanical strength | Rope 6.4 times 2.5 kN at its clipped eye; estimate 2.08 kN (unverified); hanger rating per bin | Rope 4 times; hanger rated | Not verifiable at TRL 3 |
| R8 | Power autonomy | 7.7 days with no sun and the fan continuous (relay input 3 mA or less, a purchase check); refill from 50 % in 3.5 days with the 20 W panel and 85 % charge efficiency; mast south of the bin (D13) | 5 days; refill in 3 days | Not met (recovery; 25 W proposed) |
| R4 | Fan decision rule | Rule as specified; fan heat measured by the plenum probe within ±0.51 °C, about ±0.5 points of EMC | Rule, minimum run and off times, starts per hour | Met |
| R1 | Temperature profile | 6 levels at 0.94 m; ±0.1 to ±0.2 °C; every 10 min | 6 or more, 1.0 m or less; ±0.3 °C | Met |
| R5 | Fail-safe control | Normally open relay, stale-data timeout, hand position independent of GrainGuard | Stop in 60 s; hand runs the fan | Met |
| R7 | Radio link | 10.9 dB margin at 1 km past one building at SF10 and 500 kHz (the legal mode, D15) | 1 km, one building, 10 dB margin, 95 % delivery | Met |
| R11 | Install without grain entry | Empty-bin installation sequence | No entry into a bin holding grain | Met |
| R12 | Electrical isolation | 12 V system, charging clamped at 15.0 V; relay input 2.5 kV | 15 V or less; 2.5 kV | Met |
| R13 | Cost per bin | USD 410.50 per bin, constructable design; receiver USD 22.00 per farm | Value-engineering target USD 260 per bin, receiver per farm | Over the value-engineering target by USD 150.50 |
| R14 | Local data | Farmhouse receiver logs locally | No cloud account | Met |

## Corrections to the TRL 2 documents

- Grain in the reference bin: 123.1 m³, about 3,493 bu, 88.8 t (was about 132 m³, 3,760 bu, 95 t) [A2].
- Airflow at 0.2 cfm/bu: 0.330 m³/s, 699 cfm (was 0.36 m³/s, 760 cfm) [A3].
- Heat to cool the grain 10 °C: about 493 kWh (was about 500 kWh); fan energy per cycle about 48 kWh at 0.40 kW (was 110 kWh at an assumed 1.1 kW) [A9].
- Fan heat: 0.5 to 2.7 °C depending on the fan (was "about 1 °C") [A7].
- Hot spot coverage: 3.3 % (was about 3 %) [C2].
- Autonomy: 7.7 days with the fan continuous and the 3 mA relay input (was 4.8 days) [D5]; recovery 3.5 days with the 20 W panel and the charge efficiency (2.9 days without it in version 0.6) [D6].
- Radio margin: 10.9 dB at 1 km past a building with the modelled antenna at 500 kHz, the legal mode (16.9 dB at 125 kHz in version 0.6; about 48 dB over free space at 2 km at TRL 2) [E3].
- Cost: $247.00 per bin at TRL 3 (was about $271); $256.50 with the plenum probe adopted under GGD-DDR-002 [H1], [H3].
