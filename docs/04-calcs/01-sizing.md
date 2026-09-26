---
doc_id: GGD-CAL-001
title: GrainGuard sizing calculations
project: GrainGuard
doc_type: Calculation
version: "0.3"
status: Draft
date: '2026-09-26'
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
---

# GrainGuard sizing calculations

On paper, GrainGuard meets eight of its fourteen requirements, has three at risk, misses one, and has two that cannot be verified at TRL 3. The miss is power (R8): with the relay input specified at 3 mA the battery now lasts 7.7 days with no sun, but a 10 W panel needs about 7.3 winter days, not 3, to refill the battery from half charge. Cost (R13) is now met: Amish adopted the plenum temperature probe into the base kit on 2026-09-25 (GGD-DDR-002), which took the per-bin kit from $247.00 to $256.50, $6.50 over the former $250 budget, and on 2026-09-26 he set the budget to $260 to cover it, with the farmhouse receiver costed per farm. In return the fan's own heat, worth about one point of moisture per degree, is now measured, and the fan decision (R4) moves from at risk to met. The three at risk are the moisture estimate (R2), heating detection away from the center (R6) and the environment (R9). The calculations also corrected three TRL 2 figures: the reference bin holds about 88.8 t, not 95 t, because the aeration floor sits 0.4 m above the pad; the fan heat of "about 1 °C" is right only for a 0.4 kW fan; and the radio margin at 1 km past a building is about 18 dB, not 48 dB. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [A3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace the bin maker's roof and hanger ratings, a licensed electrician's design of the starter interface, or a confined-space entry procedure. Nothing may be installed in a bin on the strength of this note. GrainGuard must never be used to judge whether a bin is safe to enter. See GGD-PRC-001, Safety.

## Scope and method

The note checks every requirement in GGD-REQ-001 v0.4 against the design in GGD-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()`, so the bin, pod positions, rope length, cable route and mast dimensions used here are the ones in the STEP files and on drawing GGD-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes the requirement table to `docs/04-calcs/results.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

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
| Power | Controller 25 mW; pod bus 0.72 W for 3 s every 10 min; LoRa 0.15 W for 0.37 s every 10 min; charge controller 6 mA; relay input 3 mA at 12 V; 7 Ah AGM, 50 % usable, 60 % of that at -20 °C; winter 1.5 peak sun hours, 60 % derating | As at TRL 2, except the relay input (was 10 mA) |
| Radio | 14 dBm, -132 dBm at SF10 and 125 kHz, 0 dBi antennas, 1 dB cable loss each end; antennas 2.4 m (mast) and 2.0 m (farmhouse); 20 dB for one farm building; plane-earth path loss | Typical SX1262 figures; building loss assumed |
| Cable loads | Janssen pressures with K 0.5 and wall friction 0.4; grain on steel 0.3; pod drag = vertical pressure on the pod face plus side friction; unloading overpressure factor 2.0 | Screening values, not a bin-load standard |
| Mast | 45 m/s gust (1,215 Pa); drag coefficient 1.2 on the panel and 1.0 on the shield; mast pinned at the stay; S235 pipe | Screening values |

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

- **Autonomy.** The TRL 2 design had a 10 mA relay input and used 5.30 Wh per day with the fan running continuously [D2]. The 7 Ah AGM battery gives 25.2 Wh usable at -20 °C [D4], so it lasted 4.8 days. With the relay input specified at 3 mA or less (an optically isolated input, BOM item 11), daily use falls to 3.28 Wh and autonomy rises to 7.7 days with the fan continuous and 9.3 days at 8 h per day [D3], [D5]. The autonomy half of R8 is met with no added cost.
- **Recovery.** At 1.5 winter peak sun hours the 10 W panel yields 9.0 Wh per day, a net 5.7 Wh with the fan continuous, and needs 7.3 days to refill 42 Wh from half charge; at 2.5 peak sun hours it needs 3.6 days [D6]. Refilling in 3 days at 1.5 peak sun hours would take a panel of about 19 W [D7]. The recovery half of R8 is **not met**, so R8 is **not met**. A 20 W panel would add about $8 to $10 and take the kit over budget; the choice is open (see `docs/REVIEW.md`).
- **Charging voltage (R12).** A temperature-compensated AGM charger raises its absorption voltage to 15.75 V at -20 °C and 16.05 V at -30 °C, over the 15 V limit in R12. The charge controller is therefore specified with its compensation clamped at 15.0 V [D8]. With that specification R12 is **met**.

## E. Radio (R7)

- The link budget is 144 dB [E1]. The TRL 2 margin of about 48 dB used free-space loss at 2 km (97.7 dB) [E2], which is optimistic for antennas 2 m above the ground.
- With plane-earth loss at 1 km (106.4 dB, well past the 59 m breakpoint) and 20 dB for one farm building, the margin is 17.6 dB [E3]. With a 10 dB fade margin the same model gives about 1.55 km [E4]. R7 is **met** on paper; the 95 % delivery figure needs a site survey.
- A packet of 24 bytes takes 371 ms at SF10, inside the 400 ms dwell limit in the US 915 MHz band; 25 bytes would take 412 ms [E5]. The payload is therefore limited to 24 bytes.

## F. Cable loads and mast (R10)

- **Pull-down force.** Janssen's method gives 25.8 kPa vertical and 12.9 kPa lateral pressure at the floor [F1]. The static drag is 213 N on the rope and 825 N on the six pods, 1,038 N in all, and about 2,076 N with an unloading overpressure factor of 2.0 [F2]. The TRL 2 design force of 2.5 kN is kept, 1.2 times this estimate [F3]. The measured maximum of 4.7 kN on the largest commercial cable ([Illinois Experts, ASABE](https://experts.illinois.edu/en/publications/forces-on-monitoring-cables-during-grain-bin-filling-and-emptying/)) is consistent with a larger cable in a larger bin.
- **Rope.** A 20 kN rope gives a factor of 8.0 on 2.5 kN against R10's 4 [F3]. The roof hanger rating comes from the bin maker, bin by bin, so R10 as a whole is **not verifiable at TRL 3**.
- **Mast.** At a 45 m/s gust, the panel and shield put 128 N and 31 N on the mast, a moment of 108 N·m at the stay. The DN25 pipe (section modulus 2.14 cm³) sees 50 MPa, 4.7 times below yield [F4].
- **Lengths.** The rope hangs 6.62 m and the bus cable route is 14.6 m, 6.5 m of it inside the bin [G1]. The BOM carries 16 m of bus cable.

## G. Environment (R9)

Lead-acid electrolyte freezes near -25 °C at 50 % state of charge and below -50 °C when full (typical manufacturer tables, to confirm on the chosen battery's datasheet) [G2]. At the -30 °C lower limit of R9, the low-voltage disconnect must keep the battery well above half charge, which cuts the usable energy assumed in section D. Phosphine resistance of the pods is still unverified. R9 is **at risk**.

## H. Cost (R13)

- The per-bin kit (items 1 to 11, 13 and 14) costs $256.50, 1.3 % ($3.50) under the $260 budget [H1]. The TRL 2 cost of about $271 fell to $247.00 after the cost trims decided in GGD-DDR-001 (D1): SHT40 sensors in the four middle pods, a smaller enclosure, and bus cable cut to the model's route length. The plenum probe ($9.50), adopted into the kit by Amish with its $6.50 overrun against the former $250 budget accepted (GGD-DDR-002), adds the rest [H3]. Amish approved the budget on 2026-09-26 and `budget_usd` is now $260 (GGD-DDR-002), so R13 is **met** (it was not met, overrun accepted, in v0.2).
- The farmhouse receiver adds $22.00 once per farm; a first prototype with one bin costs $278.50 [H2].

## Requirement status

*Table 3. Status of every requirement in GGD-REQ-001 v0.4 [I1], [I2]. Not met items first.*

| ID | Requirement | Value at TRL 3 | Target | Status |
| --- | --- | --- | --- | --- |
| R8 | Power autonomy | 7.7 days with no sun and the fan continuous; refill from 50 % in 7.3 days | 5 days; refill in 3 days | **Not met** |
| R2 | Moisture estimate | Sensor-only error 0.23 points (SHT45) and 0.42 points (SHT40) worst case; 0.81 at the SHT40 maximum; equation error not included | ±0.8 points, 20 % to 75 % RH | At risk |
| R6 | Heating alert | Center core only, 3.3 % of the section; latency about 13 min | Any pod, alarm within 15 min | At risk |
| R9 | Environment | AGM may freeze near -25 °C at 50 % charge; phosphine unverified | -30 °C to +50 °C; IP66; one fumigation | At risk |
| R3 | Ambient air | SHT45 ±0.1 °C and ±1.0 % RH; shield error unknown | ±0.3 °C, ±2 % RH | Not verifiable at TRL 3 |
| R10 | Mechanical strength | Rope 8 times 2.5 kN; estimate 2.08 kN; hanger rating per bin | Rope 4 times; hanger rated | Not verifiable at TRL 3 |
| R4 | Fan decision rule | Rule as specified; fan heat measured by the plenum probe within ±0.51 °C, about ±0.5 points of EMC | Rule, minimum run and off times, starts per hour | Met |
| R1 | Temperature profile | 6 levels at 0.94 m; ±0.1 to ±0.2 °C; every 10 min | 6 or more, 1.0 m or less; ±0.3 °C | Met |
| R5 | Fail-safe control | Normally open relay, stale-data timeout, hand position independent of GrainGuard | Stop in 60 s; hand runs the fan | Met |
| R7 | Radio link | 17.6 dB margin at 1 km past one building | 1 km, one building, 95 % delivery | Met |
| R11 | Install without grain entry | Empty-bin installation sequence | No entry into a bin holding grain | Met |
| R12 | Electrical isolation | 12 V system, charging clamped at 15.0 V; relay input 2.5 kV | 15 V or less; 2.5 kV | Met |
| R13 | Cost per bin | $256.50 per bin with the plenum probe; receiver $22.00 per farm | $260 per bin, receiver per farm | Met (budget approved by Amish, 2026-09-26; not met, overrun accepted, in v0.2) |
| R14 | Local data | Farmhouse receiver logs locally | No cloud account | Met |

## Corrections to the TRL 2 documents

- Grain in the reference bin: 123.1 m³, about 3,493 bu, 88.8 t (was about 132 m³, 3,760 bu, 95 t) [A2].
- Airflow at 0.2 cfm/bu: 0.330 m³/s, 699 cfm (was 0.36 m³/s, 760 cfm) [A3].
- Heat to cool the grain 10 °C: about 493 kWh (was about 500 kWh); fan energy per cycle about 48 kWh at 0.40 kW (was 110 kWh at an assumed 1.1 kW) [A9].
- Fan heat: 0.5 to 2.7 °C depending on the fan (was "about 1 °C") [A7].
- Hot spot coverage: 3.3 % (was about 3 %) [C2].
- Autonomy: 7.7 days with the fan continuous and the 3 mA relay input (was 4.8 days) [D5]; recovery not met [D6].
- Radio margin: 17.6 dB at 1 km past a building (was about 48 dB over free space at 2 km) [E3].
- Cost: $247.00 per bin at TRL 3 (was about $271); $256.50 with the plenum probe adopted under GGD-DDR-002 [H1], [H3].
