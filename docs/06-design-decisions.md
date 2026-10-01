---
doc_id: GGD-DEC-001
title: GrainGuard design decisions register
project: GrainGuard
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from GGD-DDR-001, GGD-DDR-002, the review note and the design for construction (GGD-DDR-003)
---

# GrainGuard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the changes that make the design buildable | (a) accept GGD-DDR-003 as drafted; (b) accept with changes | (a): every change keeps what GrainGuard does, and the model passes all 374 constructability checks | The whole build plan follows GGD-DDR-003 | GGD-DDR-003 |
| 2 | Battery and panel capacity for the recovery half of R8 (refill from half charge in 3 winter days) | (a) a 20 W panel (about USD 8 to 10 more; panel bracket and wind load to recheck); (b) relax the target to about 7 days; (c) accept the miss | None recorded | Panel, panel bracket (section 3.12), charge controller rating | GGD-DDR-001 O2, GGD-DDR-002 |
| 3 | Pitch wording against the cool-mode rewet bound (at most 74 kg of water per cycle) | (a) keep "without rewetting it"; (b) say only "cool it or dry it"; (c) cut the cool-mode allowance to zero | None recorded | Controller settings only; no hardware | GGD-DDR-002 O4 |
| 4 | First host farm and electrician for a co-design visit | A farm with a small corn bin and an aeration fan in the US Midwest, and its electrician | None recorded (partners are to be picked per area later) | Where the prototype is built; the bin's own stiffener, hanger and cap | GGD-DDR-001 O1 |
| 5 | How the pods are protected against phosphine fumigation | (a) conformal coating only; (b) coating plus sealed connectors; (c) pods lifted out before each fumigation | (a) for the prototype, with a coupon of coated board left in the bin through one fumigation at TRL 4 | Pod board coating (section 3.1, step 6) | GGD-PRC-001, open questions; R9 |
| 6 | Charge controller low-voltage disconnect setting | A setting that keeps the AGM battery above about 50 % charge in deep cold, so it cannot freeze near -25 °C | Set it to the battery maker's figure for 50 % at -20 °C (about 12.1 V), confirm at TRL 4 | Charge controller set-up (section 3.11) | GGD-CAL-001 G2; R9 |
| 7 | Appearance model and photoreal renders | (a) bring `cad/src/product_model.py` into line with GGD-DDR-003 and re-render on Amish's Mac; (b) leave the renders showing the concept | (a), at the next render session | None (media only) | Review note 2026-09-26, items 1, 4, 5 and 6; GGD-DDR-003 |
| 8 | Control rule defaults and target moisture values | Confirm with an extension specialist and a host farmer | Confirm before automatic mode is first used | Controller settings only | GGD-PRC-001, open questions |

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought or the site is chosen.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The bin maker rates the center hanger for cable loads, and for at least the 2.5 kN design pull-down | The rope hangs from it; an unrated roof can buckle (R10) | GGD-CAL-001 F3; build plan S3 |
| 2 | The position and spacing of two stiffener bolts at a sheet seam between 1.4 and 1.8 m up, near the mast position | They set the wall bracket's holes and the stay height; the mast lug must match | GGD-DDR-003 P5 |
| 3 | The peak cap is fixed (it does not lift for filling) and has room for an M12 gland 300 from the axis | The bus cable leaves through it; if the cap lifts, the cable goes through a roof panel next to it instead | GGD-DDR-003 P4 |
| 4 | The enclosure's lug kit, lug spacing and inner boss positions | They set the mounting plate's lug holes and the battery shelf position | GGD-DDR-003 P6 |
| 5 | The solar panel frame has a flat back lip at least 12 wide | The panel bolts through it | GGD-DDR-003 P7 |
| 6 | The mast clamps' V-saddles fit 33.7 mm (DN25) pipe and take 3 to 4 mm plate | Every part on the mast hangs on them | GGD-DDR-003 P5 to P8 |
| 7 | The charge controller can clamp its temperature compensation at 15.0 V | Keeps the system at 15 V or less in the cold (R12) | GGD-CAL-001 D8 |
| 8 | The fan transition top is sheet steel thin enough for an M12 gland, with room 300 out from the wall clear of access panels | The plenum probe goes there | GGD-DDR-002; build plan step 14 |
| 9 | The antenna's connector matches the board's, and the coax loss is 1 dB or less at 915 MHz | The radio margin assumes 1 dB of cable loss at each end (R7) | GGD-CAL-001 E1 |

## Value engineering

Value-engineering target: USD 260 (a hypothetical control target, not a limit; `budget_usd` in `project.yaml`). Estimated cost of the constructable design: USD 389.50 per bin (USD 129.50 over the target), with the farmhouse receiver (USD 22.00) costed once per farm. The concept kit was USD 256.50; making it buildable added USD 133.00 (GGD-DDR-003, GGD-CAL-001 H1 and H4).

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
| 2026-09-30 | Make the design physically buildable while drawing the build plan; changes recorded as Draft for review (see open decision 1) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | GGD-DDR-003 |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a limit; cost is reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register; GGD-CAL-001 v0.4 |
