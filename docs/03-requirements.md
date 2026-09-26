---
doc_id: GGD-REQ-001
title: GrainGuard requirements
project: GrainGuard
doc_type: Requirements
version: "0.4"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 decisions (GGD-DDR-001); R13 redefined per bin with the receiver per farm; R4 plenum EMC basis; reference case corrected; status from GGD-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R4 restated with the plenum probe in the base kit; R13 status records the accepted $6.50 overrun; status from GGD-CAL-001 v0.2
---

# GrainGuard requirements

These requirements were checked by calculation at TRL 3 in GGD-CAL-001. Targets are not yet validated with farmers and will be revised after co-design visits (see GGD-PRB-001). One requirement is not met (R8, battery recovery), one is missed by an overrun that Amish has accepted (R13, $6.50 over), three are at risk (R2, R6, R9) and two cannot be verified at TRL 3 (R3, R10); Table 2 gives the status of each. Version 0.3 recorded the decisions in GGD-DDR-001: R13 is redefined per bin with the farmhouse receiver costed per farm (D1), and R4 states how the plenum-air EMC is found (D3, D9). Version 0.4 records GGD-DDR-002: the plenum probe is in the base kit, so R4 uses the measured plenum temperature and is met on paper, and the $6.50 cost overrun it causes is accepted.

The **reference case** is a 5.49 m (18 ft) diameter corrugated steel bin with a 5.6 m eave above the pad, a full perforated floor 0.4 m above the pad and grain level with the eave (5.2 m deep): about 88.8 t (3,493 bu) of shelled corn stored at a target of 15.0 % moisture, wet basis, in the US Midwest (GGD-DDR-001, D11), with one existing aeration fan giving about 0.330 m³/s (699 cfm, 0.2 cfm/bu).

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Grain temperature profile | 6 or more levels on one center cable, 1.0 m or less apart; ±0.3 °C; one reading every 10 min | Sensor datasheet; geometry check in the model |
| R2 | Grain moisture estimate from interstitial air | Within ±0.8 percentage points, wet basis, for interstitial RH of 20 % to 75 % and grain at 0 °C to 30 °C, from readings taken 6 h or more after the fan stops | EMC error analysis with sensor tolerance; later comparison with oven or meter samples |
| R3 | Ambient air measurement | ±0.3 °C and ±2 % RH inside a radiation shield; sampled every 5 min; decisions on 30 min averages | Datasheet and shield error estimate |
| R4 | Fan decision rule | Automatic mode runs the fan only when the plenum-air EMC (from the ambient humidity ratio and the plenum temperature, measured by the plenum probe in the fan transition, BOM item 14) is at or below the target moisture (hold mode), or when plenum air is 5 °C or more below the mean grain temperature and its EMC is no more than 1.0 point above target (cool mode); minimum run 30 min, minimum off 15 min, 4 starts per hour or fewer | Logic review against extension guidance; later simulation over a season of weather data |
| R5 | Fail-safe control | In automatic mode the fan stops within 60 s of controller power loss or when sensor data are more than 30 min old; the hand position of the hand-off-auto switch runs the fan with GrainGuard removed; fan running is confirmed by current within 30 s and a mismatch raises an alarm | Circuit review; later bench test |
| R6 | Heating alert | Alarm at the farmhouse within 15 min when any pod rises 3 °C or more above its 7-day minimum with the fan off, or sits 5 °C or more above the bin median | Logic review; later heated-core test |
| R7 | Radio link | Bin to farmhouse over 1 km or more with one farm building in the path; 95 % or more of packets delivered | Link budget; later site survey |
| R8 | Power autonomy | 5 days or more with no solar input at -20 °C with the fan running continuously; recovers from 50 % charge to full in 3 winter days of 1.5 peak sun hours | Power budget |
| R9 | Environment | Operate at -30 °C to +50 °C; controller IP66; pods dust-tight (IP6X) with a vapor-permeable membrane; survive one phosphine fumigation per season | Datasheets and design review; later exposure test |
| R10 | Mechanical strength | Rope minimum breaking load 4 times or more the design pull-down force of 2.5 kN (estimate); roof hanger rated by the bin maker for the design force | Force estimate; bin maker's data |
| R11 | Install and service without grain entry | Installed with the bin empty, from the roof manhole and floor under a confined-space and fall-protection procedure; no GrainGuard task needs anyone in a bin that holds grain | Installation sequence review |
| R12 | Electrical isolation | Controller, cable and pods at 15 V DC or less; the relay kit is the only mains-connected item, installed by a licensed electrician, with 2.5 kV or more isolation between control input and contacts | Circuit review; relay datasheet |
| R13 | Affordable | $250 or less in parts per bin, with the farmhouse receiver (one per farm) costed per farm and excluded; priced options excluded | Priced BOM (`bom/bom.csv`) |
| R14 | Local data | All readings and fan hours stored on the farm; no cloud account needed | Architecture review |

*Table 2. Status at TRL 3 (GGD-CAL-001 v0.2, Table 3). Not met items first.*

| ID | Status at TRL 3 | Basis |
| --- | --- | --- |
| R8 | **Not met** | Autonomy 7.7 days with the fan continuous and a 3 mA relay input (met); refill from 50 % takes 7.3 days with the 10 W panel (not met); a panel of about 19 W would meet it (open, GGD-DDR-001 O2) |
| R13 | **Not met, overrun accepted** | $256.50 per bin with the plenum probe, $6.50 (2.6 %) over $250; receiver $22.00 per farm; overrun accepted by Amish (GGD-DDR-002) |
| R2 | At risk | Sensor-only error 0.23 points (SHT45) and 0.42 points (SHT40) worst case over 20 % to 75 % RH, 0.81 at the SHT40 maximum tolerance; equation fit error, drift and membrane lag not included |
| R6 | At risk | Alarm latency about 13 min (met); only the center core, 3.3 % of the cross-section, is watched |
| R9 | At risk | AGM electrolyte may freeze near -25 °C at 50 % charge; phosphine protection unverified |
| R3 | Not verifiable at TRL 3 | SHT45 meets the target; the radiation error of the shield needs a test |
| R10 | Not verifiable at TRL 3 | Rope 8 times the 2.5 kN design force (estimate 2.08 kN); the roof hanger rating comes from the bin maker |
| R4 | Met | Rule met by design; fan heat measured by the plenum probe within ±0.51 °C, so the plenum EMC is known within about ±0.5 points (GGD-CAL-001, B10) |
| R1 | Met | Six pods at 0.94 m pitch; ±0.1 °C (SHT45) and ±0.2 °C (SHT40) typical |
| R5 | Met | Normally open relay, stale-data timeout and hand-off-auto switch |
| R7 | Met | 17.6 dB margin at 1 km past one farm building (plane-earth model); 24-byte packets fit the 400 ms dwell limit |
| R11 | Met | Empty-bin installation sequence in GGD-PRC-001 |
| R12 | Met | 12 V system with charging clamped at 15.0 V; optically isolated relay input |
| R14 | Met | Farmhouse receiver stores data locally |

## Assumptions

- Grain properties: shelled corn at 721 kg/m³ (25.4 kg per 0.0352 m³ bushel) and a specific heat of about 2.0 kJ/(kg·K) at 15 % moisture.
- EMC from the ASABE D245.6 modified Henderson equation for corn; accuracy of RH-based moisture prediction as reported by [USDA ARS](https://www.ars.usda.gov/ARSUserFiles/30200525/362AccuracyGrainMoistureContentPrediction.pdf).
- The fan warms the air by its input power over the air's heat capacity rate: about 1.0 °C for a 0.40 kW fan, 0.5 to 2.7 °C for 0.2 to 1.1 kW (GGD-CAL-001, section A).
- Cooling front time of 75 to 119 h at 0.2 cfm/bu, from extension guidance and a sensible-heat balance.
- Design pull-down force of 2.5 kN for a thin 6 mm cable is kept; GGD-CAL-001 estimates about 2.08 kN with an unloading overpressure factor of 2.0. Forces up to 4.7 kN were measured on the largest commercial cable during unloading ([Illinois Experts, ASABE](https://experts.illinois.edu/en/publications/forces-on-monitoring-cables-during-grain-bin-filling-and-emptying/)); thinner cables see less force, but this is unverified.
