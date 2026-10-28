---
doc_id: GGD-OPT-001
title: GrainGuard concept options
project: GrainGuard
doc_type: Concept options
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: "First issue (kit 1.8 upgrade): the current design as option A and two options with different working principles, each modelled at detail level D3 (kit 1.9); weighted scoring against GGD-URS-001; all three within 10 %, so all go to Amish without a pick"
---

# GrainGuard concept options

All three options score within 10 % of each other, so no option is recommended and the choice goes to Amish: option A, the center sensor cable (193 of 245), option C, the fan-side weather controller (192), and option B, the headspace sensor head (186). The close scores hide a sharp split. Option A is the only one that measures the grain itself and meets PR-001 (temperature profile), PR-002 (moisture) and, in part, PR-006 (heating alarm), the needs GrainGuard exists for; option C is less than half the cost and keeps everyone on the ground, but it is a weather-driven fan schedule that never sees the grain. Option A stays the design of record, as the current design of a repo designed before kit 1.8 must (STANDARDS section 21), until Amish decides; options B and C would change the pitch, which is his call in any case. The choice is recorded as "Proposed, awaiting Amish" in GGD-DEC-001 (open item 10) and argued in GGD-DDR-004. Method: STANDARDS section 21.

![Concept options side by side at one scale](../media/options.png)

*Figure 1. The three options at one scale with a 1.75 m person, rendered from the D3 models in `cad/src/model.py` (`components(option)`) with `python .kit/options.py`. The bin, fan and starter are the existing farm equipment of the reference case.*

## The options

### Option A: center sensor cable with EMC fan control (the current design)

Six temperature and humidity pods on a 6 mm wire rope hang down the bin axis from the bin's center hanger and read the grain itself; a solar 12 V controller on a mast by the bin runs the fan through an electrician-installed relay kit only when the plenum air's equilibrium moisture content (EMC), with the fan heat measured by a plenum probe, will cool or dry the grain. This is the constructable design of GGD-PRC-001, GGD-DDR-003 and the build plan GGD-BLD-001. It measures the temperature profile at 0.94 m pitch and estimates moisture from interstitial RH within 0.23 to 0.42 points from the sensors alone (GGD-CAL-001 B5). Its risks are the moisture estimate's unknown fit error (PR-002), a center cable that watches only 3.3 % of the cross-section (PR-006), the battery in deep cold (STEM check S17) and the roof load during unloading, which depends on the bin maker's hanger rating (PR-010). It needs from a co-design partner a host bin with a rated center hanger, a farmer to set crop targets and an electrician for the relay kit. D3 model: 331 parts (147 fasteners, 19 weld beads), 27.7 kg in `cad/fidelity.json`.

### Option B: headspace sensor head with CO₂ watch

No cable in the grain. A printed sensor head, 124 mm across, carrying an SHT45, an NDIR CO₂ module and a small aspirating fan, hangs from the bin's center hanger by an eye bolt in the existing shackle, just under the peak, and reads the air leaving the grain: during a fan run that air carries the top layer's temperature and equilibrium RH, and when grain starts to spoil the headspace CO₂ rises (a Purdue field trial saw 500 to 5,000 ppm as a tank spoiled; STEM check B2). The bus cable leaves through the same peak-cap gland and runs down the wall to a wall unit: a 3 mm aluminium backplate held 0.3 m off the wall stiffener by two welded wall arms on the stiffener's own seam bolts, carrying option A's enclosure, solar panel and radiation shield, so no mast or anchors are needed. Plenum probe, relay kit and conduit are as in option A. It puts almost nothing on the roof hanger, and the head can be reached from the roof with the bin full. It gives no temperature profile and only a bin-top moisture average (B3), its ambient sensor sits close to a sunlit wall, and its wall arms need a calculation and the bin maker's bolt rating (B4). It needs the same partners as A, plus an extension specialist to set CO₂ alarm thresholds for corn. D3 model: 275 parts (150 fasteners, 16 weld beads), 18.9 kg.

### Option C: fan-side weather controller

No sensor in the bin. A small IP66 controller on the starter's post, powered from the relay kit's 24 V supply, runs the fan on outside-air EMC (the same rule as A, with the plenum probe measuring the fan heat) and counts fan hours against a cooling-front model (75 to 119 h a cycle; GGD-CAL-001 A8) to judge when a front has passed. The ambient sensor sits in a radiation shield on an arm at the post top. It needs no solar panel, no battery, no mast, no roof work and no bin entry, and it costs less than half of option A. It is a schedule, not a measurement: it cannot see a hot spot, a wet layer or a front that has not passed (C2), so PR-001, PR-002 and PR-006 are not met, and it stops when the starter's supply is isolated. Commercial weather-only aeration controllers and a farmer-built smart-switch system exist (GGD-MKT-001), so its open-hardware value would be cost and documentation. D3 model: 111 parts (45 fasteners), 7.3 kg.

## First-order numbers

Table 1. Options compared (costs are estimates for one bin; option A's is the priced BOM).

| Quantity | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Estimated parts cost (USD) | 410.50 (BOM) | about 370 (estimate: A less the rope, pods and mast, plus the sensor head and the wall unit) | about 170 (estimate: controller, ambient shield, relay kit, probe and short conduit; no panel, battery, mast or cable) |
| Against the USD 260 value-engineering target | USD 150.50 over | about USD 110 over | about USD 90 under |
| Mass in the D3 model (kg) | 27.7 | 18.9 | 7.3 |
| What it measures | Grain temperature at 6 levels, interstitial RH (moisture), ambient, plenum | Headspace T, RH and CO₂ (bin-top average), ambient, plenum | Ambient and plenum only |
| Energy | 3.28 Wh per day from a 20 W panel and a 7 Ah AGM battery | About the same plus the head's fan and CO₂ module (to size) | Under 1 W from the starter's 24 V supply |
| Parts in the D3 model (fasteners) | 331 (147) | 275 (150) | 111 (45) |
| Install work | Empty-bin entry and roof work for the cable; mast on the pad | Roof work only; wall unit on the stiffener | At the starter post only |
| STEM check | Within known science; S17 fix proposed | Within known science; B3, B4 plausible | Within known science as a schedule; C2 plausible |

## Scoring

Table 2. Weighted scoring (weights: High UR 3, Medium 2, Low 1; scores 1 to 5). UR-013 (cost) is scored on the cost row.

| Criterion | Source | Weight | A | B | C | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| Grain temperature through the depth | UR-001 | 3 | 5 | 1 | 1 | Only A measures the grain at levels; B reads the headspace, C nothing in the bin |
| Drying or rewetting | UR-002 | 3 | 4 | 2 | 1 | A estimates moisture at each pod (at risk); B gives a bin-top average after fan runs; C only predicts |
| Outside air at the bin | UR-003 | 2 | 4 | 3 | 4 | A and C keep the shield in open air; B's shield is 0.3 m from a sunlit wall |
| Fans run only when they help | UR-004 | 3 | 5 | 4 | 3 | All use plenum EMC; A's cool mode uses measured grain temperature, B the headspace, C a model |
| Safe when the controller fails | UR-005 | 3 | 5 | 5 | 5 | Same normally open relay, timeout and hand position |
| Warning of heating | UR-006 | 3 | 3 | 4 | 1 | A sees heating near the center only; B's CO₂ sees spoilage anywhere that vents to the headspace; C cannot |
| Status from the farmhouse | UR-007 | 2 | 5 | 5 | 5 | Same LoRa link and receiver |
| No mains, all winter | UR-008 | 3 | 4 | 4 | 4 | A and B solar with the south siting rule; C needs the starter's supply, which every aerated bin has, but stops when it is isolated |
| Survives the bin's conditions | UR-009 | 3 | 3 | 3 | 4 | A and B carry a lead-acid battery (S17) and electronics in the fumigant; C has neither |
| No damage to the roof | UR-010 | 3 | 3 | 5 | 5 | A's cable pulls on the hanger during unloading; B's head weighs about a kilogram; C has nothing on the roof |
| No entry into a bin holding grain | UR-011 | 3 | 4 | 5 | 5 | A is installed with the bin empty and its pods cannot be reached when full; B's head is reached from the roof; C stays at the starter |
| Mains work kept small | UR-012 | 3 | 5 | 5 | 4 | C also draws its power from the relay kit's supply, so a little more mains-side work |
| Data stays on the farm | UR-014 | 2 | 5 | 5 | 5 | Same receiver |
| Retrofit, workshop built | UR-015 | 2 | 4 | 3 | 5 | A has one welded mast; B two welded wall arms and two stiffener seams; C bought parts and one bent arm |
| Repairable | UR-016 | 1 | 4 | 4 | 5 | All bought modules; C has the fewest parts |
| Legal radio | UR-017 | 2 | 5 | 5 | 5 | Same radio and packet |
| Cost against the value-engineering target | UR-013 | 2 | 1 | 2 | 5 | USD 410.50, about USD 370 and about USD 170 against USD 260 |
| Buildable with local skills and tools | | 2 | 3 | 3 | 5 | A and B need welding, printing and wiring; C wiring and one bent arm |
| Safety | | 3 | 3 | 4 | 5 | A needs empty-bin entry and roof work, B roof work, C ground work only |
| Maintenance | | 1 | 3 | 4 | 5 | A's pods are out of reach while the bin is full |
| **Weighted total (of 245)** | | | **193** | **186** | **192** | All within 10 % (B is 3.6 % below A) |

## Recommendation

No pick: the three options are within 10 % of each other, so all three go to Amish (STANDARDS section 21), recorded as "Proposed, awaiting Amish" in GGD-DEC-001 open item 10 and argued in GGD-DDR-004. Option A remains the design of record until he decides, and the pitch ("Cable of moisture and temperature probes strung through the bin") describes option A only.

The observation for his decision: the weighted sum lets options B and C make up on cost, safety and simplicity what they lose on the three measurements GrainGuard is for. If PR-001, PR-002 and PR-006 are treated as must-haves, only option A passes. If the farmer's first need is cheap, safe fan control and spoilage detection can come later, option C is the cheaper start, and option B is the way to detect spoilage without a cable.

The runner-up ideas worth grafting onto option A, whichever way he decides:

- From option C: where the starter is within reach, power the controller from the relay kit's 24 V supply instead of the panel and battery. That would remove the USD 76 of panel, battery and charge controller, the battery's freezing problem (S17) and its hydrogen (S18), at the cost of a powered cable from the starter to the mast.
- From option B: the headspace CO₂ head as the priced option already allowed for in GGD-DDR-001 (D10), hung from the same shackle above the cable, to see spoilage beyond the center core that one cable cannot watch (PR-006).
