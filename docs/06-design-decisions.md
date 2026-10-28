---
doc_id: GGD-DEC-001
title: GrainGuard design decisions register
project: GrainGuard
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from GGD-DDR-001, GGD-DDR-002, the review note and the design for construction (GGD-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations of open items 1 to 8 on 2026-10-02; all moved to decisions made; panel and charge controller lines to confirm updated
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Follow-ups carried out (20 W panel and adjustable-disconnect controller in the BOM and model; cost USD 406.50); one new open decision, the stay-off service limit
  - version: "0.4"
    date: '2026-10-24'
    author: Amish Chadha
    change: "Kit 1.8 and 1.9 upgrade: STEM check fixes D10 and D12 to D17 decided under the standing instruction of 2026-10-23 (D12 closes open item 9); D3 model fit details D11; open items 10 (concept selection, no pick), 11 (battery disconnect against cold) and 12 (winter recovery); confirm items 10 to 17; cost USD 410.50"
---

# GrainGuard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1a. Open decisions.*

| No. | Question | Options | Recommendation |
| --- | --- | --- | --- |
| 10 | Concept selection between the three options of GGD-OPT-001 (GGD-DDR-004) | (A) center sensor cable with EMC fan control, 193 of 245, the current design. (B) headspace sensor head with CO₂ watch, 186. (C) fan-side weather controller, 192. B and C would change the pitch | None: all three within 10 %, so no pick (STANDARDS section 21). Option A stays the design of record until Amish decides; only A meets PR-001, PR-002 and, near the center, PR-006. Grafts worth a separate decision: the 24 V supply from the relay kit (from C) and the headspace CO₂ head (from B) |
| 11 | The battery's low-voltage disconnect against cold. At the 50 % figure decided on 2026-10-02 (item 6) the electrolyte freezes near -20 °C (BCI table; AGM somewhat lower), above the -30 °C of PR-009 (STEM check S17, GGD-CAL-001 G3) | (a) The battery maker's 65 % figure: freezes near -30 °C (no margin); 5.4 days with no sun on the conservative basis, 9.0 at the station's low draw. (b) The 70 % figure: freezes near -36 °C; 4.6 days conservative, 7.7 at low draw. (c) Keep 50 % and restate PR-009 to -20 °C. (d) A larger battery with the 70 % figure (size and cost to check) | (b), with the AGM maker's freezing data and a cold-chamber autonomy test at TRL 4: a 6 K margin against freezing, and an empty battery stops the fan (the safe state) while a frozen one cracks; it changes Amish's 2026-10-02 setting, so it is his decision |
| 12 | Winter recovery of PR-008. With an 85 % lead-acid charge efficiency (missing until the independent review) the 20 W panel decided on 2026-10-02 (item 2) refills from half charge in 3.5 days at 1.5 peak sun hours, not 3 (STEM check S14, GGD-CAL-001 D6, D7) | (a) A 25 W panel: 2.7 days; panel bracket and mast checks rerun (stay-off limit about 27 m/s); a few dollars more (estimate). (b) Restate the target to 3.5 days. (c) An MPPT controller in place of PWM, recovering part of the mismatch inside the 0.6 derating (to quantify). (d) A charge controller with 2 mA self-use: 3.2 days, still short | (a), with the 1.5 peak sun hours confirmed from NREL data for the host site |

Decided under Amish's standing instruction of 2026-10-23 and moved to Table 3: open item 9 (the stay-off service limit, by D12).

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought or the site is chosen.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The bin maker rates the center hanger for cable loads, and for at least the 2.5 kN design pull-down | The rope hangs from it; an unrated roof can buckle (R10) | GGD-CAL-001 F3; build plan S3 |
| 2 | The position and spacing of two stiffener bolts at a sheet seam between 1.4 and 1.8 m up, near the mast position | They set the wall bracket's holes and the stay height; the mast lug must match | GGD-DDR-003 P5 |
| 3 | The peak cap is fixed (it does not lift for filling) and has room for an M12 gland 300 from the axis | The bus cable leaves through it; if the cap lifts, the cable goes through a roof panel next to it instead | GGD-DDR-003 P4 |
| 4 | The enclosure's lug kit, lug spacing and inner boss positions | They set the mounting plate's lug holes and the battery shelf position | GGD-DDR-003 P6 |
| 5 | The solar panel (20 W, decided 2026-10-02) has a frame with a flat back lip at least 12 wide, and its size fits the panel bracket | The panel bolts through it; the bracket was drawn for the 10 W panel and is now 430 mm wide for a panel of about 430 x 350 mm | GGD-DDR-003 P7; decision of 2026-10-02 (open item 2) |
| 6 | The mast clamps' V-saddles fit 33.7 mm (DN25) pipe and take 3 to 4 mm plate | Every part on the mast hangs on them | GGD-DDR-003 P5 to P8 |
| 7 | The charge controller can clamp its temperature compensation at 15.0 V, and has an adjustable low-voltage disconnect that can be set to the battery maker's 50 % figure at -20 °C (about 12.1 V) | Keeps the system at 15 V or less in the cold (R12) and the battery from freezing (R9) | GGD-CAL-001 D8 and G2; decision of 2026-10-02 (open item 6) |
| 8 | The fan transition top is sheet steel thin enough for an M12 gland, with room 300 out from the wall clear of access panels | The plenum probe goes there | GGD-DDR-002; build plan step 14 |
| 9 | The antenna's connector matches the board's, and the coax loss is 1 dB or less at 915 MHz | The radio margin assumes 1 dB of cable loss at each end (R7) | GGD-CAL-001 E1 |
| 10 | The two M16 labyrinth vents have a clear bore of 10 mm or more and an ingress rating of IP55 or better | Battery hydrogen ventilation (D10, STEM check S18) and PR-009 | GGD-CAL-001 G4 |
| 11 | The mast tube is EN 10255 medium series (S195T) or better, and the four M10 anchors' tension rating in the pad's concrete covers 1.83 kN with margin | Mast and anchor checks (D12, STEM check S23, S24, S26) | GGD-CAL-001 F4 to F6 |
| 12 | The host bin has a mast position within 30 degrees of due south of its axis, 0.7 m out from the wall, near a stiffener with seam bolts at 1.4 to 1.8 m, with no other building or tree shading the panel in winter and clear of snow sliding off the roof | The panel must not be shaded (D13); roof snow (STEM check S33) | GGD-CAL-001 G5 |
| 13 | The AGM maker's freezing point at the chosen disconnect setting | Open item 11 | GGD-CAL-001 G3 |
| 14 | The relay kit's optically isolated input draws 3 mA or less at 12 V (a coil relay held on draws 30 to 70 mA) | Autonomy of PR-008 rests on it (STEM check S13) | GGD-CAL-001 D3 |
| 15 | Winter insolation at the host site at a 45 degree tilt facing south, from NREL data, against the 1.5 peak sun hours assumed | PR-008 recovery (open item 12) | GGD-CAL-001 D6 |
| 16 | The wall bracket's two refitted stiffener bolts and the stiffener carry the stay's 397 N with the bin maker's agreement | The stay holds the mast (STEM check review) | GGD-CAL-001 F5 |
| 17 | The charge controller's 15.0 V clamp tolerance | PR-012 battery bus limit (STEM check S16) | GGD-CAL-001 D8 |

## Value engineering

Value-engineering target: USD 260 (a hypothetical control target, not a limit; `budget_usd` in `project.yaml`). Estimated cost of the constructable design: USD 410.50 per bin (USD 150.50 over the target), including the two battery vents of D10 (USD 4.00, an estimate), the 20 W panel (USD 34.00, USD 9.00 more) and the adjustable-disconnect charge controller (USD 18.00, USD 8.00 more) decided on 2026-10-02, with the farmhouse receiver (USD 22.00) costed once per farm. The concept kit was USD 256.50; making it buildable added USD 133.00, the 2026-10-02 decisions USD 17.00 and the vents USD 4.00 (GGD-DDR-003, GGD-CAL-001 H1 and H4). Option C's graft (power from the relay kit's 24 V supply where the starter is near) would remove the panel, battery and charge controller, USD 76 (GGD-OPT-001).

Main cost drivers:

- The mast weldment, stay, wall bracket, anchors and six mast clamps: USD 53.00 (the concept costed USD 15.00 for a mast with no joints).
- The six pods: USD 67.00 together, of which the glands, gasket, screws and rope stops added for construction are USD 21.00.
- The relay kit with its post mount: USD 39.00; the radio and bus board: USD 30.00.
- Three lines missing from the concept: antenna USD 15.00, battery fuse and surge protection USD 12.00, conduit USD 12.00.

Savings worth trying:

- Mount the controller box, panel and shield on the wall stiffener instead of a mast: saves roughly USD 40 (mast weldment, anchors, stay and two clamps), but the panel's facing is then set by which side of the bin the stiffener is on, and the ambient sensor sits close to the wall's reflected heat, so it changes the concept and would need Amish's decision.
- Fit the antenna directly on the box with a sealed bulkhead: saves about USD 8; the radio margin falls to about 12 dB at 1 km, still meeting R7.
- Crimped ferrule stops instead of set-screw rope stops: about USD 10 for six, where a swaging tool is available.
- Direct-burial-rated cable clipped along the wall foot instead of conduit: about USD 8.
- Buy cable, clamps and fixings for several bins at once: the per-bin cost of lines 3, 10 and 13 falls with quantity.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D11: budget per bin with the receiver per farm and cost trims, pitch reword, control rule and defaults, RH-based moisture sensing, one center cable with six pods, RS-485 pod bus, solar controller with an electrician-installed relay kit, AGM battery, plenum sensing if affordable, CO₂ as an option, corn in a small Midwest bin | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | GGD-DDR-001 |
| 2026-09-25 | Plenum temperature probe adopted into the base kit; relay input of 3 mA or less; charger clamped at 15.0 V | Amish: "i accept all your recommendations, go with them across all repos." | GGD-DDR-002, N1 to N3 |
| 2026-09-26 | Budget set to USD 260 to cover the priced BOM | Amish: "i approve all the budget items." | GGD-DDR-002 v0.2 |
| 2026-09-27 | Solar panel faces away from the bin, out of the wall's shade | Amish: "resolve the challenges for ConePro, BridgePulse, Grainguard and WellSense." | GGD-DDR-002 v0.3 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; changes recorded as Draft for review (accepted on 2026-10-02, below) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | GGD-DDR-003 |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a limit; cost is reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; GGD-CAL-001 v0.4 |
| 2026-10-02 | Open item 1: design for construction accepted: GGD-DDR-003 as drafted | Amish: "i approve your recommendations for all 555 open decisions." | GGD-DDR-003 |
| 2026-10-02 | Open item 2: battery and panel capacity for the recovery half of R8: fit a 20 W panel, provided the mast check with the stay removed is rerun for the larger panel and still passes | Amish: "i approve your recommendations for all 555 open decisions." | GGD-DDR-001 O2; GGD-DDR-002 |
| 2026-10-02 | Open item 3: the pitch says only "cool it or dry it" (no "without rewetting it"), and the cool-mode allowance is kept | Amish: "i approve your recommendations for all 555 open decisions." | GGD-DDR-002 O4 |
| 2026-10-02 | Open item 4: first host farm and electrician: recruit the host farm and its electrician through a land-grant extension grain-storage specialist, for example at Purdue University or Iowa State University, choosing a farm with a small corn bin, an aeration fan and a center hanger. This is the route to the first candidate, not an agreed partner | Amish: "i approve your recommendations for all 555 open decisions." | GGD-DDR-001 O1 |
| 2026-10-02 | Open item 5: phosphine protection: conformal coating for the prototype, with a coated test board left in the bin through one fumigation at TRL 4; move to sealed connectors if that board shows copper corrosion | Amish: "i approve your recommendations for all 555 open decisions." | GGD-PRC-001, open questions; R9 |
| 2026-10-02 | Open item 6: a charge controller with an adjustable low-voltage disconnect, set to the battery maker's 50 % figure at -20 °C (about 12.1 V); confirmed at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | GGD-CAL-001 G2; R9 |
| 2026-10-02 | Open item 7: the appearance model is brought into line with GGD-DDR-003 and re-rendered on Amish's Mac at the next render session | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, items 1, 4, 5 and 6; GGD-DDR-003 |
| 2026-10-02 | Open item 8: the control rule defaults and target moistures are confirmed with the extension specialist of item 4 and the host farmer before automatic mode is first used | Amish: "i approve your recommendations for all 555 open decisions." | GGD-PRC-001, open questions |
| 2026-10-24 | D10: two M16 labyrinth vents (10 mm clear bore, IP55 or better), one in the enclosure's bottom face in place of the M12 membrane breather and one at the top of its left side wall (its centre 15 below the top, so no gas pocket is left above it), so battery hydrogen leaves by natural draught; BOM line 4 USD 20.00 to USD 24.00 (estimate); PR-009 restated (IP66 except at the vents). Options weighed: a fan (needs power and a control), a separate vented battery box (more parts, colder battery), a larger membrane vent (no open area, does not meet the method) | Claude, under Amish's standing instruction of 2026-10-23 (STEM check S18); Amish can reverse it | GGD-DDR-005; GGD-STM-001 S18; GGD-CAL-001 G4 |
| 2026-10-24 | D11: fit details found by the D3 model of kit 1.9 and fixed in the model, the BOM descriptions and the build plan: (1) the five jumper cables run 8 mm further out than the main run, so where one arrives at a pod and the next leaves they lie side by side instead of crossing in one place; (2) the battery shelf's two M5 screws are countersunk (ISO 10642) so the battery's back sits flat on the shelf; (3) the charge controller hangs on a flange with two M4 screws into the inner plate; (4) the radio board stands on four M3 nylon standoffs, screwed from both sides of the inner plate; (5) the fuse, surge protector and terminal strip clip onto a 60 mm top-hat rail with two M4 screws. No design dimension changed | Claude, under Amish's instruction of 2026-09-30 to make the design physically buildable, as design-for-construction details | GGD-DDR-005; `cad/src/ggd_detail.py` |
| 2026-10-24 | D12: the mast is checked at the 195 MPa yield of S195T, the grade of EN 10255 33.7 x 3.2 tube (was 235 MPa), and the stay comes off only in gusts under 30 m/s, on a calm day, and is refitted before leaving (114 MPa, 1.7 times yield). Closes open item 9 with its recommended option (a); a DN32 mast would not reach the 1.5 times margin at 45 m/s either (about 140 MPa against 130 MPa) | Claude, under Amish's standing instruction of 2026-10-23 (STEM check S23 and S24); Amish can reverse it | GGD-DDR-005; GGD-CAL-001 F4 to F6 |
| 2026-10-24 | D13: the mast stands on the south side of the bin, within 30 degrees of due south of the bin axis (north side in the southern hemisphere), so the bin never shades the panel; at 42 °N the noon sun is 24.6 degrees up at the winter solstice and the wall's shadow is 12.3 m long. Added to the build plan (step 5) and the precis | Claude, under Amish's standing instruction of 2026-10-23 (STEM check S15); Amish can reverse it | GGD-DDR-005; GGD-CAL-001 G5 |
| 2026-10-24 | D14: PR-012 reworded: the 15 V limit applies to the battery bus, the controller's outputs, the bus cable and the pods; the panel circuit runs below 30 V open circuit (extra-low voltage). No hardware change | Claude, under Amish's standing instruction of 2026-10-23 (STEM check S16, independent review) | GGD-DDR-005; GGD-PRS-001 |
| 2026-10-24 | D15: the radio runs at SF10 with a 500 kHz bandwidth on one channel at both ends, the digital modulation route of 47 CFR 15.247(a)(2); a fixed 125 kHz channel is not a legal mode. Firmware setting; BOM lines 5 and 12 described; link margin 16.9 to 10.9 dB at 1 km (PR-007 still met). Options weighed: hopping over 50 channels (needs a multichannel or synchronised receiver), a multichannel gateway (cost) | Claude, under Amish's standing instruction of 2026-10-23 (STEM check S20, independent review) | GGD-DDR-005; GGD-CAL-001 E |
| 2026-10-24 | D16: the controller zeroes the plenum probe against the ambient sensor whenever the fan has been off for an hour, so the probe's offset below its rated -10 °C does not reach the decision rule. Firmware only | Claude, under Amish's standing instruction of 2026-10-23 (STEM check S31, independent review) | GGD-DDR-005 |
| 2026-10-24 | D17: a 0.5 A fuse on the bus cable's 12 V feed at the surge strip, so a short in the 0.34 mm² cores inside the bin clears before the cable heats; within BOM line 16's price (estimate) | Claude, under Amish's standing instruction of 2026-10-23 (STEM check S32, independent review) | GGD-DDR-005 |
