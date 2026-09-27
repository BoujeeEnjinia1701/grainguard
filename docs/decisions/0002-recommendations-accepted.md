---
doc_id: GGD-DDR-002
title: GrainGuard recommendations accepted
project: GrainGuard
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-09-27'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all recommendations and the changes made in the repo
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: "Budget set to $260 to cover the priced BOM: decided by Amish, 2026-09-26; R13 met"
- version: "0.3"
  date: '2026-09-27'
  author: Amish Chadha
  change: "Solar panel faces away from the bin: decided by Amish on 2026-09-27; model.py rotation sign flipped, drawing GGD-DWG-001 Rev P3"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below that carried a recommendation is "Decided by Amish, 2026-09-25: go with recommendation". Items without a recommendation remain "Proposed, awaiting Amish". The budget was decided by Amish on 2026-09-26 (see Budget, 2026-09-26). The solar panel facing was decided by Amish on 2026-09-27 (see Solar panel facing, 2026-09-27).

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." After GGD-DDR-001, GrainGuard had one open item with a recommendation (O3, the plenum probe), two component specifications set in GGD-CAL-001 v0.1 and flagged for Amish (a relay input of 3 mA or less and a charger clamped at 15.0 V), two open items with no recommendation (O1 and O2) and one question on the pitch wording with options but no recommendation. Where a recommendation offered several options, the recommended option is the decision. TRL 4 remains on hold by Amish's instruction, and the repo stays at TRL 3.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 to D11 | TRL 2 review items (GGD-DDR-001): budget option (a), pitch reword, control rule, RH sensing, one center cable, RS-485, solar controller with relay kit, AGM, plenum sensing if affordable, CO₂ as an option, corn in a small Midwest bin | Already decided in GGD-DDR-001; confirmed | No change |
| N1 (was O3) | Adopt the plenum temperature probe despite the budget | Adopt it into the base kit and accept the $6.50 overrun | `bom/bom.csv` item 14 is no longer an option. Per-bin kit $247.00 to $256.50 (2.6 % over $250); first prototype with receiver $269.00 to $278.50. `budget_usd` stays $250, and R13 records the accepted overrun (status "not met, overrun accepted"), following the recommendation to accept rather than raise the budget. GGD-CAL-001 v0.2 adds check B10: with a DS18B20 (±0.5 °C) and the ambient SHT45 (±0.1 °C), the fan heat is known within ±0.51 °C and the plenum EMC within about ±0.50 points, against a 1.85-point spread when the fan heat is only a setting. R4 moves from at risk to met on paper and is restated in GGD-REQ-001 v0.4. GGD-PRC-001 v0.4, drawing GGD-DWG-001 Rev P2 (notes), concept media (labels, key figures, flow) and `cad/src/model.py` comment updated; STEP and STL re-exported (geometry unchanged, the probe was already modeled) |
| N2 | Relay input of 3 mA or less (flagged in GGD-CAL-001 v0.1) | Keep as specified | No change; recorded in GGD-PRC-001 v0.4, Key design choices |
| N3 | Charger compensation clamped at 15.0 V (flagged in GGD-CAL-001 v0.1) | Keep as specified | No change; recorded in GGD-PRC-001 v0.4, Key design choices |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First host farm and electrician for a co-design visit. No partner was recommended. | Proposed, awaiting Amish |
| O2 | Battery and panel capacity for the recovery half of R8: a 20 W panel (about $8 to $10, further over budget), relax the recovery target to about 7 days, or accept the miss. No recommendation was made. | Proposed, awaiting Amish |
| O4 | Pitch wording against the cool-mode rewet bound (at most 74 kg of water per cycle, one point in the bottom 0.37 m): keep "without rewetting it", say only "cool it or dry it", or cut the cool-mode allowance to zero. No recommendation was made. | Proposed, awaiting Amish |

*Table 3. Decided but on hold.*

| Item | Status |
| --- | --- |
| TRL 4 work named in the review note (bench pod and plenum probe with a lab test report, membrane equilibration time, fan heat on a real fan, relay kit fail-off timing, cold-soak of battery and charger, build log entries) | Decided as the next step, on hold: TRL 4 is on hold by Amish's instruction |

No cross-repo action arises: GrainGuard does not use SwapCell or any other portfolio module.

### Budget, 2026-09-26

On 2026-09-26 Amish wrote: "i approve all the budget items." Budget set to $260 to cover the priced BOM: decided by Amish, 2026-09-26. The priced per-bin kit is $256.50 (`bom/bom.csv`, items 1 to 11, 13 and 14, with the farmhouse receiver costed per farm under GGD-DDR-001 D1), so `budget_usd` in `project.yaml` moves from 250 to 260. This supersedes the N1 choice to keep $250 and record the overrun: R13 moves from "not met, overrun accepted" to met. `docs/04-calcs/sizing.py` reads the budget from `project.yaml` and was rerun; GGD-CAL-001 v0.3, GGD-REQ-001 v0.5, GGD-PRC-001 v0.5, GGD-PRB-001 v0.4, `README.md` and `bom/bom-notes.md` were updated. Requirement status is now met 8, at risk 3, not met 1 (R8) and not verifiable 2.

### Solar panel facing, 2026-09-27

On 2026-09-27 Amish wrote: "resolve the challenges for ConePro, BridgePulse, Grainguard and WellSense." For GrainGuard the challenge was item 2 of the appearance-model review (docs/REVIEW.md, session 2026-09-26): `cad/src/model.py` rotated the solar panel envelope with `Rot(0, -panel_tilt, 0)`, which tilts its face toward the bin, although its comment says "facing away from the bin"; 0.7 m from a 5.6 m wall the panel would then sit in the wall's shade. The recommendation was to change the rotation to `Rot(0, panel_tilt, 0)` and regenerate the media. Decided by Amish on 2026-09-27: go with the recommendation.

- `cad/src/model.py`: the panel rotation is now `Rot(0, panel_tilt, 0)`, so the face tilts 45 degrees from horizontal toward the outside of the bin (local +X). Panel size, tilt angle, height and position on the mast are unchanged.
- `cad/src/product_model.py`: the appearance model already faced the panel away from the bin with the same rotation. Its comment that model.py "rotates its envelope box the other way" was removed; its pose now matches model.py with no compensation.
- Regenerated: STEP and STL (`cad/step`, `cad/stl`), drawing GGD-DWG-001 Rev P3 (detail B and the views show the panel facing outward) and the concept media (`media/hero.png`, `concept-blueprint`, `cutaway.png`, `exploded.png`, `flow.png`, `model.glb`).
- GGD-PRC-001 v0.6 states the facing in its component table. No requirement status changes: the R8 energy figures in GGD-CAL-001 already assumed a panel in sun, and the wind load uses the panel area, which is unchanged.

## Consequences

- Requirement status (GGD-CAL-001 v0.2): not met 1 (R8); not met with an accepted overrun 1 (R13); at risk 3 (R2, R6, R9); not verifiable at TRL 3 2 (R3, R10); met 7 (R1, R4, R5, R7, R11, R12, R14). Before this record: not met 1, at risk 4, not verifiable 2, met 7.
- Controlled documents bumped: GGD-PRC-001 v0.4, GGD-REQ-001 v0.4, GGD-CAL-001 v0.2, GGD-DDR-001 v0.2; drawing GGD-DWG-001 Rev P2.
- `project.yaml`: `budget_usd` stayed 250 under N1 (set to 260 on 2026-09-26, see above), pitch and problem unchanged, `trl: 3` and `trl_target: 3` unchanged.
