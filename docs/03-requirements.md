---
doc_id: GGD-REQ-001
title: GrainGuard requirements
project: GrainGuard
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
---

# GrainGuard requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with farmers, and will be checked by calculation at TRL 3 and revised after co-design visits (see GGD-PRB-001). Three requirements are not met by the current concept (R8, R10 roof capacity, R13), and two are at risk (R6 coverage, R9 fumigation); Table 2 gives the status of each.

The **reference case** is a 5.49 m (18 ft) diameter corrugated steel bin with a 5.6 m eave and a full perforated floor, filled with about 95 t (3,760 bu) of shelled corn stored at a target of 15.0 % moisture, wet basis, with one existing aeration fan giving about 0.36 m³/s (760 cfm, 0.2 cfm/bu).

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Grain temperature profile | 6 or more levels on one center cable, 1.0 m or less apart; ±0.3 °C; one reading every 10 min | Sensor datasheet; geometry check in the model |
| R2 | Grain moisture estimate from interstitial air | Within ±0.8 percentage points, wet basis, for interstitial RH of 20 % to 75 % and grain at 0 °C to 30 °C, from readings taken 6 h or more after the fan stops | EMC error analysis with sensor tolerance; later comparison with oven or meter samples |
| R3 | Ambient air measurement | ±0.3 °C and ±2 % RH inside a radiation shield; sampled every 5 min; decisions on 30 min averages | Datasheet and shield error estimate |
| R4 | Fan decision rule | Automatic mode runs the fan only when the predicted plenum-air EMC is at or below the target moisture (hold mode), or when plenum air is 5 °C or more below the mean grain temperature and its EMC is no more than 1.0 point above target (cool mode); minimum run 30 min, minimum off 15 min, 4 starts per hour or fewer | Logic review against extension guidance; later simulation over a season of weather data |
| R5 | Fail-safe control | In automatic mode the fan stops within 60 s of controller power loss or when sensor data are more than 30 min old; the hand position of the hand-off-auto switch runs the fan with GrainGuard removed; fan running is confirmed by current within 30 s and a mismatch raises an alarm | Circuit review; later bench test |
| R6 | Heating alert | Alarm at the farmhouse within 15 min when any pod rises 3 °C or more above its 7-day minimum with the fan off, or sits 5 °C or more above the bin median | Logic review; later heated-core test |
| R7 | Radio link | Bin to farmhouse over 1 km or more with one farm building in the path; 95 % or more of packets delivered | Link budget; later site survey |
| R8 | Power autonomy | 5 days or more with no solar input at -20 °C with the fan running continuously; recovers from 50 % charge in 3 winter days | Power budget |
| R9 | Environment | Operate at -30 °C to +50 °C; controller IP66; pods dust-tight (IP6X) with a vapor-permeable membrane; survive one phosphine fumigation per season | Datasheets and design review; later exposure test |
| R10 | Mechanical strength | Rope minimum breaking load 4 times or more the design pull-down force of 2.5 kN (estimate); roof hanger rated by the bin maker for the design force | Force estimate; bin maker's data |
| R11 | Install and service without grain entry | Installed with the bin empty, from the roof manhole and floor under a confined-space and fall-protection procedure; no GrainGuard task needs anyone in a bin that holds grain | Installation sequence review |
| R12 | Electrical isolation | Controller, cable and pods at 15 V DC or less; the relay kit is the only mains-connected item, installed by a licensed electrician, with 2.5 kV or more isolation between control input and contacts | Circuit review; relay datasheet |
| R13 | Affordable | $250 or less in parts per bin | Priced BOM (`bom/bom.csv`) |
| R14 | Local data | All readings and fan hours stored on the farm; no cloud account needed | Architecture review |

*Table 2. Status of the concept against each requirement (estimates, see GGD-PRC-001).*

| ID | Status at TRL 2 | Basis |
| --- | --- | --- |
| R1 | Met on paper | Six SHT45 pods at 1.0 m pitch; ±0.1 °C typical sensor accuracy |
| R2 | Met on paper for 20 % to 75 % RH; not met above about 80 % RH | Published EMC prediction error of 0.25 to 0.65 points (dry basis) with ±2 % RH sensors; error grows fast above 70 % to 80 % RH, that is for wet grain |
| R3 | Met on paper | Sensor accuracy; shield error unverified |
| R4 | Met by design | Rule in GGD-PRC-001 |
| R5 | Met by design | Normally open relay and hand-off-auto switch |
| R6 | At risk | Met for the center core only; heating more than about 0.5 m from the cable is not detected |
| R7 | Met on paper | About 48 dB of margin over free space at 2 km (estimate) |
| R8 | **Not met** | About 4.8 days with the fan running continuously; about 7.6 days at 8 h of fan time per day |
| R9 | At risk | Phosphine corrodes copper; pod and connector protection unverified |
| R10 | Rope met; **roof capacity not met until confirmed** | 6 mm rope about 20 kN, 8 times the design force; older bin roofs may not have a rated hanger |
| R11 | Met by design | Installation sequence in GGD-PRC-001 |
| R12 | Met by design | Solar 12 V controller; DIN relay kit |
| R13 | **Not met** | About $271 per bin, about $293 with the shared farmhouse receiver |
| R14 | Met by design | Farmhouse receiver stores data locally |

## Assumptions

- Grain properties: shelled corn at 721 kg/m³ (25.4 kg per 0.0352 m³ bushel) and a specific heat of about 1.9 kJ/(kg·K).
- EMC from the ASABE D245.6 modified Henderson equation for corn; accuracy of RH-based moisture prediction as reported by [USDA ARS](https://www.ars.usda.gov/ARSUserFiles/30200525/362AccuracyGrainMoistureContentPrediction.pdf).
- The fan warms the air about 1 °C (estimate); to be measured at TRL 3.
- Cooling front time of 75 to 120 h at 0.2 cfm/bu, from extension guidance and a sensible-heat balance.
- Design pull-down force of 2.5 kN for a thin 6 mm cable is an estimate. Forces up to 4.7 kN were measured on the largest commercial cable during unloading ([Illinois Experts, ASABE](https://experts.illinois.edu/en/publications/forces-on-monitoring-cables-during-grain-bin-filling-and-emptying/)); thinner cables see less force, but this is unverified.
