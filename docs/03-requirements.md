---
doc_id: GGD-PRS-001
title: GrainGuard product requirements and specifications
project: GrainGuard
doc_type: Product requirements
version: "0.9"
status: Draft
date: '2026-10-24'
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
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Design for construction (GGD-DDR-003); R13 reported against the value-engineering target (Amish, 2026-10-01); R7 margin from the modelled antenna"
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: R8 and R9 status notes record the 2026-10-02 decisions (GGD-DEC-001, items 2, 5 and 6); no status changed
- version: "0.9"
  date: '2026-10-02'
  author: Amish Chadha
  change: Status from GGD-CAL-001 v0.6; R8 not met to met with the 20 W panel (stay-off service rule proposed); R13 USD 406.50 per bin
- version: "0.9"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.8 upgrade: migrated from GGD-REQ-001 to GGD-PRS-001; R1 to R14 become PR-001 to PR-014 with tolerance, units and the user need each traces to (GGD-URS-001); PR-015 added (retrofit and workshop build); status from GGD-CAL-001 v0.7 and the STEM check GGD-STM-001: PR-008 not met (winter recovery with the charge efficiency) and PR-009 not met (battery electrolyte at -30 °C), fixes proposed; PR-007 radio route (D15), PR-009 vents (D10), PR-012 wording (D14); cost USD 410.50"
---

# GrainGuard product requirements and specifications

What the design must do, each traced to a user need in GGD-URS-001. On paper, GrainGuard meets eight of its fifteen product requirements; two are **not met** (PR-008, winter recovery: with a lead-acid charge efficiency the 20 W panel refills the battery in 3.5 days, not 3, GGD-DEC-001 open item 12; PR-009: with the low-voltage disconnect at the 50 % figure decided on 2026-10-02 the battery's electrolyte freezes near -20 °C, above the -30 °C asked, open item 11; both fixes proposed to Amish), two are at risk (PR-002 moisture, PR-006 heating away from the center), two can be verified only at TRL 4 (PR-003, PR-010), and cost (PR-013) is reported against the value-engineering target: USD 410.50 per bin against USD 260, USD 150.50 over. The targets are proposals until a co-design visit with a farmer and an extension specialist (GGD-DEC-001, item 4 of 2026-10-02). This document replaces GGD-REQ-001 (kit 1.8, STANDARDS section 22); each requirement keeps its target, verification and status, and its old number is in the "Was" column. Method: STANDARDS section 22.

The **reference case** is a 5.49 m (18 ft) diameter corrugated steel bin with a 5.6 m eave above the pad, a full perforated floor 0.4 m above the pad and grain level with the eave (5.2 m deep): about 88.8 t (3,493 bu) of shelled corn stored at a target of 15.0 % moisture, wet basis, in the US Midwest (GGD-DDR-001, D11), with one existing aeration fan giving about 0.330 m³/s (699 cfm, 0.2 cfm/bu).

Table 1. Product requirements and specifications (status from GGD-CAL-001 v0.7, Table 3, and GGD-STM-001).

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Grain temperature profile | The kit shall measure grain temperature at 6 or more levels on one center cable, 1.0 m or less apart, every 10 min | 6 levels, 1.0 m pitch, 10 min | ±0.3 °C per sensor | levels, m, min | Analysis and inspection (GGD-CAL-001 C1, model), TRL 3 | Met on paper | R1 |
| PR-002 | UR-002 | Performance | Grain moisture estimate | The kit shall estimate grain moisture from interstitial air for 20 % to 75 % RH and grain at 0 °C to 30 °C, from readings taken 6 h or more after the fan stops | 0.8 | ± (max) | percentage points, wet basis | Analysis (GGD-CAL-001 B5), TRL 3; comparison with oven or meter samples, TRL 4 | At risk | R2 |
| PR-003 | UR-003 | Performance | Ambient air measurement | The kit shall measure outside air inside a radiation shield every 5 min and decide on 30 min averages | ±0.3 °C, ±2 % RH | max | °C, % RH | Datasheet and shield error estimate; shield error test, TRL 4 | To verify at TRL 4 | R3 |
| PR-004 | UR-004 | Software | Fan decision rule | Automatic mode shall run the fan only when the plenum-air EMC, from the ambient humidity ratio and the measured plenum temperature, is at or below target (hold mode), or when plenum air is 5 °C or more below the mean grain temperature with an EMC no more than 1.0 point above target (cool mode); minimum run 30 min, minimum off 15 min | 4 starts per hour or fewer | max | starts/h | Logic review (GGD-CAL-001 B10), TRL 3; season simulation, TRL 4 | Met by design | R4 |
| PR-005 | UR-005 | Safety | Fail-safe control | In automatic mode the fan shall stop within 60 s of controller power loss or of sensor data older than 30 min; the hand position runs the fan with GrainGuard removed; running is confirmed by current within 30 s | 60 | max | s | Circuit review, TRL 3; bench test, TRL 4 | Met by design | R5 |
| PR-006 | UR-006 | Performance | Heating alert | The kit shall alarm at the farmhouse within 15 min when any pod rises 3 °C or more above its 7-day minimum with the fan off, or sits 5 °C or more above the bin median | 15 | max | min | Logic review (GGD-CAL-001 C4), TRL 3; heated-core test, TRL 4 | At risk | R6 |
| PR-007 | UR-007, UR-017 | Electrical | Radio link | The bin station shall reach the farmhouse over 1 km or more with one farm building in the path with a 10 dB margin, deliver 95 % or more of packets, and operate under 47 CFR 15.247(a)(2) with a 500 kHz bandwidth (GGD-DEC-001 D15) | 1.0 km; 10 dB | min; min | km, dB | Link budget (GGD-CAL-001 E3 to E6), TRL 3; site survey, TRL 4 | Met on paper | R7 |
| PR-008 | UR-008 | Electrical | Power autonomy | The station shall run 5 days or more with no solar input at -20 °C with the fan held on, and recover from 50 % charge to full in 3 winter days of 1.5 peak sun hours, with the mast sited south of the bin (GGD-DEC-001 D13) | 5 days; 3 days | min; max | days | Power budget (GGD-CAL-001 D5, D6, G5), TRL 3 | Not met | R8 |
| PR-009 | UR-009 | Materials | Environment | The kit shall operate at -30 °C to +50 °C; controller IP66 with two labyrinth battery vents of IP55 or better (GGD-DEC-001 D10); pods dust-tight (IP6X) with a vapor-permeable membrane; survive one phosphine fumigation per season | -30 to +50 | range | °C | Datasheets and design review (GGD-CAL-001 G2 to G4), TRL 3; exposure test, TRL 4 | Not met | R9 |
| PR-010 | UR-010 | Safety | Mechanical strength | The rope's minimum breaking load shall be 4 times or more the design pull-down force of 2.5 kN (estimate); the roof hanger shall be rated by the bin maker for the design force | 4 | min (factor) | ratio | Force estimate (GGD-CAL-001 F2, F3), TRL 3; bin maker's data per bin | To verify at TRL 4 | R10 |
| PR-011 | UR-011 | Safety | Install and service without grain entry | The kit shall be installed with the bin empty, from the roof manhole and floor under a confined-space and fall-protection procedure, and no task shall need anyone in a bin that holds grain | 0 | max | entries into a bin holding grain | Installation sequence review (GGD-BLD-001), TRL 3 | Met by design | R11 |
| PR-012 | UR-012 | Electrical | Electrical isolation | The battery bus, the controller's outputs, the bus cable and the pods shall run at 15 V DC or less, and the panel circuit below 30 V open circuit (extra-low voltage; GGD-DEC-001 D14); the relay kit is the only mains-connected item, installed by a licensed electrician, with 2.5 kV or more between control input and contacts | 15 V; 2.5 kV | max; min | V, kV | Circuit review and relay datasheet (GGD-CAL-001 D8), TRL 3 | Met by design | R12 |
| PR-013 | UR-013 | Physical architecture | Cost per bin | The parts cost per bin shall be reported against the value-engineering target of USD 260 (a hypothetical control target, not a limit; Amish, 2026-10-01), with the farmhouse receiver costed per farm and priced options excluded | 260 | target | USD per bin | Priced BOM (`bom/bom.csv`; GGD-CAL-001 H1), TRL 3 | Over target | R13 |
| PR-014 | UR-014 | Software | Local data | All readings and fan hours shall be stored on the farm; no cloud account shall be needed | 0 | max | cloud accounts | Architecture review, TRL 3 | Met by design | R14 |
| PR-015 | UR-015, UR-016 | Physical architecture | Retrofit and workshop build | The kit shall fit an existing bin and fan with no welding or cutting of bin sheets and no change to the fan motor, and every made part shall be made with farm-workshop tools (saw, drill, welder or a local fabricator, 3D printer) from bought stock and modules | 0 | max | holes or welds in bin sheets (the peak cap gland excepted) | Inspection of the build plan (GGD-BLD-001) and the D3 model, TRL 3 | Met by design | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

Table 2. Basis of the status of the requirements that are not plainly met.

| Requirement | Status | Basis |
| --- | --- | --- |
| PR-002 | At risk | Sensor-only error 0.23 points (SHT45) and 0.42 points (SHT40) worst case over 20 % to 75 % RH, 0.81 at the SHT40 maximum tolerance; equation fit error, hysteresis, drift and membrane lag not included (STEM check S8) |
| PR-006 | At risk | Alarm latency about 13 min (met); only the center core, 3.3 % of the cross-section, is watched |
| PR-008 | Not met | Autonomy 7.7 days with the fan held on, if the relay input draws 3 mA or less (a purchase check); recovery from 50 % takes 3.5 days at 1.5 peak sun hours once a lead-acid charge efficiency of 85 % is included (2.9 days without it); about 23 W is needed; fix proposed to Amish: a 25 W panel (open item 12). Holds only with the mast south of the bin (D13). With the 70 % disconnect recommended for PR-009, autonomy is 7.7 days at the station's low draw or 4.6 days if the full cold derating applies |
| PR-009 | Not met | With the disconnect at the 50 % figure, the electrolyte freezes near -20 °C (BCI table; AGM somewhat lower), so -30 °C is not survived; fix proposed to Amish: the 70 % figure, freezing near -36 °C (open item 11). Battery hydrogen now vents through two labyrinth vents (D10), so the box is IP66 except at the vents (IP55 or better, to confirm). Phosphine protection by conformal coating, unverified until a coated test board goes through one fumigation at TRL 4 |
| PR-003 | To verify at TRL 4 | SHT45 meets the target; the radiation error of the shield needs a test |
| PR-010 | To verify at TRL 4 | Rope 6.4 times the 2.5 kN design force at its clipped eye (80 % termination efficiency) and 3.4 times the 4.7 kN measured on the largest commercial cable; the roof hanger rating comes from the bin maker |
| PR-013 | Over target | USD 410.50 per bin for the constructable design (GGD-DDR-003, the 2026-10-02 decisions and the vents of D10), USD 150.50 over the USD 260 target; receiver USD 22.00 per farm |

## Assumptions

- Grain properties: shelled corn at 721 kg/m³ (25.4 kg per 0.0352 m³ bushel) and a specific heat of about 2.0 kJ/(kg·K) at 15 % moisture.
- EMC from the ASABE D245.6 modified Henderson equation for corn; accuracy of RH-based moisture prediction as reported by [USDA ARS](https://www.ars.usda.gov/ARSUserFiles/30200525/362AccuracyGrainMoistureContentPrediction.pdf).
- The fan warms the air by its input power over the air's heat capacity rate: about 1.0 °C for a 0.40 kW fan, 0.5 to 2.7 °C for 0.2 to 1.1 kW (GGD-CAL-001, section A).
- Cooling front time of 75 to 119 h at 0.2 cfm/bu, from extension guidance and a sensible-heat balance.
- Design pull-down force of 2.5 kN for a thin 6 mm cable is kept; GGD-CAL-001 estimates about 2.08 kN with an unloading overpressure factor of 2.0. Forces up to 4.7 kN were measured on the largest commercial cable during unloading ([Illinois Experts, ASABE](https://experts.illinois.edu/en/publications/forces-on-monitoring-cables-during-grain-bin-filling-and-emptying/)); thinner cables see less force, but this is unverified.
