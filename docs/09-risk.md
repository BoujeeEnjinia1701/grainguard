---
doc_id: GGD-RSK-001
title: GrainGuard risk register, hazard analysis and design FMEA
project: GrainGuard
doc_type: Risk register
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: "First issue (kit 1.8 upgrade, stage P3): project risks, preliminary hazard analysis and a first-pass design FMEA"
---

# GrainGuard risk register, hazard analysis and design FMEA

The top project risk is that interstitial RH does not predict moisture well enough for the decision rule (PR-002), which a trial against oven samples settles at TRL 4. The top hazards are grain engulfment and falls while the cable is fitted, an automatic fan start during service, and the roof hanger overloaded when the bin is unloaded; the design controls each by procedure and by keeping GrainGuard's own parts at 12 V, but none can be designed out of a grain bin. The highest design FMEA numbers are the pod's moisture reading (RPN 180) and the battery in deep cold (RPN 160), the latter waiting on Amish's decision (GGD-DEC-001 open item 11). Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be found) to 5 (unlikely to be found), and the FMEA uses a 1 to 10 scale for S, O and D.

> **Safety:** Grain bins kill people. This document lists hazards so they can be controlled; it does not make any task safe. The safety notes in GGD-PRC-001 and the safety stops in GGD-BLD-001 govern every task.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | The moisture estimate misses ±0.8 points | Equation fit error, hysteresis, drift and membrane lag not quantified (STEM check S8) | Fan decisions off by about a point; PR-002 not met | 3 | 4 | Design lead | Compare pod readings with oven samples on the host farm at TRL 4; fit crop constants per lot if needed |
| P2 | No host farm and electrician found | The route through an extension specialist (decided 2026-10-02) not yet started | No co-design visit; targets stay unvalidated | 3 | 3 | Project lead | Contact a land-grant grain-storage specialist when the cap lifts |
| P3 | Bin makers will not rate their hangers for a cable | Liability; no data for a thin cable | The kit cannot be hung in many bins (PR-010) | 3 | 4 | Project lead | Ask the host bin's maker first; option B hangs almost no load (GGD-OPT-001) |
| P4 | Cost stays well over the value-engineering target | Mast, pods and relay kit; prototype quantities | Weak case against commercial systems at the low end | 4 | 2 | Design lead | Savings in GGD-DEC-001 (Value engineering); the 24 V graft from option C |
| P5 | The concept choice changes the design | Options within 10 % (GGD-DDR-004) | Rework of PRS, BOM, plan and drawings if B or C is picked | 2 | 3 | Project lead | Amish decides open item 10 before more work on option A |
| P6 | Hazardous-location rules apply inside the bin | Grain dust is a combustible dust (GGD-REG-001 A2) | Pods and cable need an assessed design | 2 | 4 | Electronics lead | Assess with a reviewer before any product claim |
| P7 | Battery freezes in a northern winter | Disconnect at the 50 % figure (S17) | Cracked battery, loss of control in the coldest weeks | 3 | 3 | Design lead | Amish decides open item 11 (recommended: the 65 % figure) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Engulfment and entrapment in grain | Entering a bin holding grain to fit or service the cable | Death by suffocation | 5 | 2 | The cable is fitted only in an empty bin, with unloading locked out, an entry permit and a trained person outside (BLD S2); no task needs entry into a bin holding grain (PR-011) | 5 x 1: procedure only; the rule must be kept |
| H2 | Fall from the bin roof | Feeding the cable and fitting the peak-cap gland | Serious injury or death | 5 | 2 | Fall protection, ladder cage and roof rail, dry calm day (BLD S3) | 5 x 1 |
| H3 | Automatic fan start | The controller starts the fan while someone works at the fan or transition | Injury from the impeller or plenum | 4 | 2 | Lock out at the disconnect; "Starts automatically" labels; the hand-off-auto switch is never a safety isolator (PRC, Safety) | 4 x 1 |
| H4 | Electric shock at the starter | Fitting the relay kit in a mains starter | Death or burns | 5 | 2 | Licensed electrician, starter isolated and locked out (BLD S6); 2.5 kV isolation; GrainGuard's own parts at 12 V (PR-012) | 5 x 1 |
| H5 | Roof overload | Grain dragging the cable during unloading | Roof buckling, falling parts | 4 | 2 | Hang only from a hanger the bin maker rates for cable loads; unload from the center (PR-010) | 4 x 2 until the rating is known |
| H6 | Battery hydrogen ignites | Gas collecting in the closed box during cold charging | Box burst, burns | 3 | 2 | Two labyrinth vents low and high (D10, 1.7 times the IEC 62485-2 opening); charge clamped at 15.0 V; fuse at the terminal | 3 x 1 |
| H7 | Battery short circuit | Wiring error or damaged lead | Burns, fire | 3 | 2 | 5 A fuse at the battery positive; fuse out until the checks (BLD) | 3 x 1 |
| H8 | Mast falls in a storm | Stay left off; anchors in weak concrete | Injury, damage | 4 | 2 | Stay off only in gusts under 30 m/s and refitted before leaving (D12); anchors to the maker's data (S26) | 4 x 1 |
| H9 | Phosphine exposure or false reassurance | Someone reads GrainGuard as a sign that a fumigated bin is safe | Poisoning | 5 | 1 | GrainGuard does not measure phosphine and says so (PRC, Safety; REG R7); only certified applicators fumigate | 5 x 1 |
| H10 | Grain dust ignition | A fault in the pods or cable in a dusty headspace | Dust fire or explosion | 5 | 1 | 12 V and a few milliamps; sealed glands; hazardous-location assessment to come (REG A2) | 5 x 1, unassessed |
| H11 | Zinc fumes when welding the mast | Welding galvanized pipe | Metal fume fever | 2 | 3 | Grind the zinc off first; weld in open air (BLD 3.4) | 2 x 1 |
| H12 | Lightning surge through the cable | Tall steel bin; cable from the roof | Damage to the controller; fire risk | 3 | 2 | Bond rope and shield to the bin; surge protector on the bus (BOM line 16) | 3 x 1 |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection, each scored 1 to 10.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Sensor pod (BOM 2) | Read grain T and interstitial RH | RH reading biased | Wrong moisture estimate; fan runs or stays off wrongly | Membrane fouled with fines; sensor drift; condensation in the pod | 6 | 5 | 6 | 180 | Compare with oven samples at TRL 4; drift check against the ambient sensor with the fan running; replaceable membrane |
| F2 | Battery (BOM 6) and disconnect (BOM 7) | Store energy through winter | Electrolyte freezes and the case cracks | Station dead in the coldest weeks; acid inside the box | Disconnect at the 50 % figure, -30 °C night (S17) | 8 | 5 | 4 | 160 | Open item 11: the 65 % figure; confirm with the AGM maker's data at TRL 4 |
| F3 | Bus cable and glands (BOM 3) | Carry 12 V and RS-485 | Cable cut or pulled out of a pod gland | Pods below the break go silent | Grain drag during unloading; rodents | 6 | 4 | 3 | 72 | Jumpers tied to the rope every 300 mm; stale-data alarm; strain relief in the glands |
| F4 | Plenum probe (BOM 14) | Measure the fan heat | Probe reads high or low | Plenum EMC off by about one point per degree | Probe out of the air stream; sheath fouled; below -10 °C its accuracy falls | 6 | 3 | 5 | 90 | Check the probe against the ambient sensor with the fan off (TRL 4); insertion depth set in the plan (48 mm) |
| F5 | Relay kit (BOM 11) | Switch the fan | Relay welded shut | Fan runs when it should not | Contact wear; inrush | 6 | 2 | 3 | 36 | Current transformer confirms fan state; mismatch alarm (PR-005) |
| F6 | Relay kit (BOM 11) | Fail off | Fan keeps running after controller power loss | Rewetting or rewarming the grain | Wrong relay type (normally closed) | 7 | 2 | 2 | 28 | Normally open relay specified; first check in the plan (PR-005) |
| F7 | Solar panel (BOM 8) | Recharge the battery | Too little winter energy | Battery runs down over weeks | Mast on the north side, shaded by the bin; snow on the panel | 7 | 3 | 4 | 84 | Mast south of the bin (D13); 45 degree tilt sheds snow; low-battery alarm |
| F8 | Enclosure and vents (BOM 4) | Keep electronics dry and vent hydrogen | Water enters through a vent | Corroded board; short circuit | Driven rain into the labyrinth vents (IP55 class) | 6 | 3 | 5 | 90 | Labyrinth vents with their openings facing down; confirm their rating from the maker; inspect at the first service |
| F9 | Mast and stay (BOM 10) | Hold panel, box, shield and antenna | Mast yields in a gust | Panel and box fall | Stay left off in a storm; S195T tube | 8 | 2 | 3 | 48 | Service rule (D12); check the stay is fitted at every visit |
| F10 | Rope and top fittings (BOM 1) | Carry the pods | Rope or hanger fails | Cable and pods fall into the grain; roof damage | Unrated hanger; corroded clips | 8 | 2 | 6 | 96 | Hang only from a rated hanger; inspect the clips at each empty-bin visit |
| F11 | Radio (BOM 5, 15) | Report to the farmhouse | Packets lost | No alarm at the house | Buildings and the bin in the path | 5 | 4 | 3 | 60 | Site survey at TRL 4; retries; stale-data alarm at the receiver |
| F12 | Pod boards (BOM 2) | Survive fumigation | Copper tracks corrode | Pods fail after a fumigation | Phosphine (S28) | 6 | 4 | 5 | 120 | Coated test board through one fumigation at TRL 4; sealed connectors if it corrodes |
