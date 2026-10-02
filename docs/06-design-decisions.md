---
doc_id: GGD-DEC-001
title: GrainGuard design decisions register
project: GrainGuard
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
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
---

# GrainGuard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought or the site is chosen.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The bin maker rates the center hanger for cable loads, and for at least the 2.5 kN design pull-down | The rope hangs from it; an unrated roof can buckle (R10) | GGD-CAL-001 F3; build plan S3 |
| 2 | The position and spacing of two stiffener bolts at a sheet seam between 1.4 and 1.8 m up, near the mast position | They set the wall bracket's holes and the stay height; the mast lug must match | GGD-DDR-003 P5 |
| 3 | The peak cap is fixed (it does not lift for filling) and has room for an M12 gland 300 from the axis | The bus cable leaves through it; if the cap lifts, the cable goes through a roof panel next to it instead | GGD-DDR-003 P4 |
| 4 | The enclosure's lug kit, lug spacing and inner boss positions | They set the mounting plate's lug holes and the battery shelf position | GGD-DDR-003 P6 |
| 5 | The solar panel (20 W, decided 2026-10-02) has a frame with a flat back lip at least 12 wide, and its size fits the panel bracket | The panel bolts through it; the bracket was drawn for the 10 W panel | GGD-DDR-003 P7; decision of 2026-10-02 (open item 2) |
| 6 | The mast clamps' V-saddles fit 33.7 mm (DN25) pipe and take 3 to 4 mm plate | Every part on the mast hangs on them | GGD-DDR-003 P5 to P8 |
| 7 | The charge controller can clamp its temperature compensation at 15.0 V, and has an adjustable low-voltage disconnect that can be set to the battery maker's 50 % figure at -20 °C (about 12.1 V) | Keeps the system at 15 V or less in the cold (R12) and the battery from freezing (R9) | GGD-CAL-001 D8 and G2; decision of 2026-10-02 (open item 6) |
| 8 | The fan transition top is sheet steel thin enough for an M12 gland, with room 300 out from the wall clear of access panels | The plenum probe goes there | GGD-DDR-002; build plan step 14 |
| 9 | The antenna's connector matches the board's, and the coax loss is 1 dB or less at 915 MHz | The radio margin assumes 1 dB of cable loss at each end (R7) | GGD-CAL-001 E1 |

## Value engineering

Value-engineering target: USD 260 (a hypothetical control target, not a limit; `budget_usd` in `project.yaml`). Estimated cost of the constructable design: USD 389.50 per bin (USD 129.50 over the target), before the 20 W panel decided on 2026-10-02 (about USD 8 to 10 more), with the farmhouse receiver (USD 22.00) costed once per farm. The concept kit was USD 256.50; making it buildable added USD 133.00 (GGD-DDR-003, GGD-CAL-001 H1 and H4).

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
