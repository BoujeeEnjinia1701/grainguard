---
doc_id: GGD-DDR-003
title: GrainGuard design for construction
project: GrainGuard
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02 as drafted
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2, as drafted, and is recorded in the design decisions register (GGD-DEC-001). Nothing here changes what GrainGuard does, its pitch or its safety case.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of GGD-DDR-002 showed what GrainGuard does but was a massing model: several parts could not be made, fixed or assembled as drawn. A build123d scan of that model (overlaps between parts, and gaps where parts should meet) found the problems in Table 1.

The changes keep what GrainGuard does: the same bin, cable position, six pods at 0.94 m, sensors, controller, battery, panel size, tilt and facing, mast position and height, enclosure, relay kit and plenum probe. Every change is in `cad/src/model.py`, which now also runs 374 constructability checks (`python cad/src/model.py --check`): no two parts overlap by more than 1 mm³, no part enters the bin, fan or starter except where it is fixed to them, and every joint in the build plan touches. All 374 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The sensor pods were solid potted shapes with the rope through the middle, and the single bus cable passed straight through all six pod bodies (39,700 mm³ of overlap). A potted pod cannot be opened, and a cable cannot pass through it without a joint. | Each pod is a printed ASA body (76 mm across, 3 mm walls, a central 14 mm rope tube, a 30 mm cone) and a printed lid on a 1 mm EPDM gasket with three M3 screws. The lid carries two M12 glands, one for the cable from above and one for the cable to the pod below; a 4-way terminal block inside joins them. The bus cable becomes one main run plus five pod-to-pod jumpers, running 48 mm beside the rope. The bottom pod's lower gland takes a blanking plug. | The pod can be opened, wired and resealed with hand tools, and the bus still reaches all six pods. The pod size, sensor position and membrane window are unchanged, so the moisture analysis (R2) is unchanged. |
| P2 | Nothing held the pods at their heights on the rope; the "clamp collar" was a solid ring with no fixing. | A stainless set-screw rope stop under each pod's tip. The pod rests on it; grain drag only ever pulls the pod down onto it. | A bought part, fitted with an Allen key; it sets the 0.94 m pitch on the rope. |
| P3 | The rope's top was a block floating at the peak, with no thimble, clips or shackle drawn. | Rope eye round a thimble, held by two wire rope clips (saddles on the long side), joined by a shackle to the eye of the bin maker's center hanger. | Standard rigging; the items were already in the BOM line. |
| P4 | The bus cable left the bin through the solid roof sheet below the peak cap (the reference roof had a closed top), then ran inside the headspace and through the wall at the eave (14,000 mm³ inside the bin shell). | The cable leaves through one M12 gland in the peak cap, 300 mm from the bin axis, square to the cap's slope; lies on the roof under stainless clips; has a drip loop and edge protector at the eave; runs down the wall 80 mm beside the stiffener at the mast; then along the stay to the mast and into the bottom of the box. Its length is 16.8 m from the model (main run 10.5 m, jumpers 5.4 m, 0.9 m of ends); 18.5 m is bought. | Matches the concept's "gland at the peak cap" with a route that does not pass through any sheet, and gives the cable support all the way. |
| P5 | The mast's base plate was drawn under the pipe with no joint, and its single round stay was a rod from the mast axis to the wall, joined at neither end. With a single pinned stay the mast would also swing along the wall. | Mast weldment: the pipe is welded to the 200 x 200 x 10 mm base plate with four 6 mm gussets and a 6 mm stay lug, then painted with zinc-rich paint. Four M10 concrete anchors. The stay is a 40 x 40 x 4 mm galvanized angle 592 mm long, bolted with two M10 bolts at each end: to the lug, and to a 60 x 60 x 5 mm wall bracket held under two existing stiffener bolts refitted 10 mm longer. A plastic cap closes the pipe top. | Two bolts at each end make the stay rigid both ways, so wind along the wall is also carried (F5: 42 MPa in the stay, 5.6 times below yield). The fixed base carries the mast alone if the stay is off for service (F6: 161 MPa, 1.5 times below yield, 1.15 kN per anchor). No new holes in the bin, as the concept required. |
| P6 | The enclosure stood 10 mm off the mast with no bracket. Inside it, the battery and the charge controller occupied the same space (71,000 mm³ of overlap). Cables entered through the top of the box. | A 3 mm aluminium mounting plate (240 x 410 mm) on two V-saddles and 1 in U-bolts; the box hangs on it by the maker's four lugs, one M5 screw each. Inside, the battery stands on a shelf of 50 x 50 x 5 mm angle, 26 mm above the floor, under a hook-and-loop strap; the charger and the LoRa board sit above it on the box's inner plate; a fuse, surge and terminal strip sits beside it. All seven cable entries are M12 glands and a vent in the bottom face, each cable looped below the box first. | Every part has a fixing; bottom entry with a drip loop is normal practice for an IP66 box outdoors (this was recommendation 3 of the 2026-09-26 appearance review). |
| P7 | The 10 W panel floated 75 mm above the mast top with no bracket. | A bracket of 3 mm aluminium, 250 mm wide, folded to 135 degrees: its upright leg sits on two V-saddles and U-bolts on the outer face of the mast top, and the panel's frame lip is bolted to its sloped leg with four M5 bolts. Panel centre now 2.24 m above the pad, same 45 degree tilt, still facing away from the bin. | The frame's back lip is the only part of a framed panel that can carry a bolt. |
| P8 | The ambient sensor's radiation shield was six solid discs fused to a rod that ran through the mast. | Six printed white ASA plates (one solid top plate, five ring plates) on three M5 rods with nylon spacers, screwed under a 40 x 40 x 4 mm aluminium angle arm 410 mm long, clamped to the side of the mast with a V-saddle and U-bolt 1.96 m up. The sensor hangs on its lead inside the stack. | Same shield size, plate count, pitch, arm length and height as the concept. |
| P9 | The relay box floated 45 mm beside the starter, and the relay signal cable and probe lead ran in a straight line across the pad and through the fan transition (42,600 mm³ inside the fan). Both cables also ran inside the mast's bore and through its base plate. | The relay box hangs on the starter's own post, directly under the starter, on the box maker's post-mount kit, joined to the starter by a short conduit nipple. Both cables run down the outside of the mast, then in a 20 mm flexible conduit (6.2 m) along the foot of the bin wall, over the top of the fan transition, and out to the relay box. The probe lead leaves the conduit through a tee on top of the transition. | Nothing crosses open pad or passes through the fan; the electrician's work stays at the starter. |
| P10 | The LoRa radio had no antenna in the model or BOM, although the radio calculation (E3) assumed an antenna 2.4 m up at the bin. | New BOM line 15: a 915 MHz whip with a bulkhead base on a bent aluminium bracket on the bin side of the mast, 2.08 m up, with a 1.5 m low-loss coax to the board. Antenna centre 2.22 m. | Recomputed with the modelled height: 16.9 dB margin at 1 km past one building (was 17.6 dB), R7 still met. |
| P11 | The safety case calls for a fuse at the battery terminal and surge protection where the bus enters the box, but neither was in the BOM. | New BOM line 16: a 5 A inline fuse at the battery positive, a surge protector on the 12 V and RS-485 lines, a terminal strip, and an earth lead from the rope and the cable shield to the bin. | Implements what GGD-PRC-001, Safety, already requires; the safety case itself is unchanged. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Calculations | GGD-CAL-001 v0.4: E3 uses the modelled antenna height (16.9 dB margin); F4 uses the modelled panel and shield heights (44 MPa at the stay, 5.3 times below yield); new F5 (stay along the wall) and F6 (mast alone, stay off); G1 cable 16.8 m and conduit 6.2 m; H1 cost. No requirement changes status except R13, now reported against the value-engineering target. | Follows the model. |
| Cost | Value-engineering target: USD 260. Estimated cost of the constructable design: USD 389.50 per bin (USD 129.50 over the target). The concept kit was USD 256.50; the parts added for construction add USD 133.00, mostly the mast weldment, stay and six clamps (USD 38.00 more), the pod glands and stops (USD 21.00), and three new lines: antenna (USD 15.00), fuse and surge protection (USD 12.00) and conduit (USD 12.00). `budget_usd` is unchanged. | Parts added for construction; see the Value engineering section of GGD-DEC-001. |
| BOM | Lines 1 to 4, 6, 8 to 11 and 13 respecified; lines 15 (antenna), 16 (fuse and surge protection) and 17 (conduit) added. | Follows the model. |
| Drawings | GGD-DWG-001 Rev P5; making sketches GGD-DWG-101 to 111 added. | Follows the model. |
| Media | Concept media regenerated from the model. The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` are made on Amish's Mac and were not regenerated; they still show the concept mast top, enclosure stand-off and pods and are now stale. | Follows the model. |

*Table 3. Items that would change what GrainGuard does.*

None. No change in this record alters what GrainGuard does, its pitch or its safety case. The design decisions register (GGD-DEC-001) carries the decisions that remain open from earlier records and the items to confirm when parts are bought.

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan GGD-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: met 7 (R1, R4, R5, R7, R11, R12, R14), at risk 3 (R2, R6, R9), not met 1 (R8), not verifiable at TRL 3 2 (R3, R10); R13 is over the value-engineering target by USD 129.50 (GGD-CAL-001 v0.4).
- The wall bracket uses two existing stiffener bolts, and the stay height is set by where those bolts are on a real bin; the peak cap gland assumes a cap that does not lift for filling. Both are items to confirm in GGD-DEC-001.
- The decisions of 2026-10-02 that follow this record (a 20 W panel on the same mast, subject to a rerun of the mast check with the stay off, and a charge controller with an adjustable low-voltage disconnect) are recorded in GGD-DEC-001.
- `cad/src/product_model.py` (the appearance model for the photoreal renders) still follows the concept and should be brought into line with this record before the renders are next made.
