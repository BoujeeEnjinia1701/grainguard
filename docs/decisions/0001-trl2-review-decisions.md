---
doc_id: GGD-DDR-001
title: GrainGuard TRL 2 review decisions
project: GrainGuard
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). O3 decided (plenum probe adopted into the base kit)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 and O2 decided by Amish on 2026-10-02 (GGD-DEC-001, items 4 and 2)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D11 and, since GGD-DDR-002, O3; items O1 and O2 were decided by Amish on 2026-10-02 as recommended in the design decisions register (GGD-DEC-001, items 4 and 2)

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eleven items as "Proposed, awaiting Amish", and the design precis GGD-PRC-001 v0.2 listed the key design choices with options and recommendations. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open. Items that arise from the TRL 3 calculations (O2 and O3) are also recorded as open.

The same instruction approved three portfolio-wide decisions: SwapCell interface v0.3 adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles; shared SwapCell packs are priced once and excluded from each dependent kit budget; and community designs pick co-design partners per area later. GrainGuard does not use SwapCell (its controller needs a few watt-hours per day at 12 V), so the first two do not apply. The third applies to O1.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in GGD-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Budget | Option (a): keep `budget_usd` at $250, cost the farmhouse receiver per farm rather than per bin, and trim the kit (SHT40 in place of SHT45 in four pods, a cheaper enclosure). R13 is redefined as "$250 or less per bin, with the farmhouse receiver costed per farm". Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Pitch wording | Reword the pitch from "runs aeration fans only when ambient air will dry the grain" to "runs aeration fans only when the air will cool or dry the grain without rewetting it", in `project.yaml` and `README.md`. The problem line is unchanged (no rewording was recommended). Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Control rule, modes and defaults | Cool and hold modes as in GGD-PRC-001: 5 °C cooling margin, 1.0-point EMC allowance in cool mode, 30 min minimum run, 15 min minimum off, 4 starts per hour or fewer, fail off. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Moisture sensing | Interstitial RH with an EMC equation, rather than capacitance probes. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Cable layout | One center cable with six pods for bins up to about 5.5 m; more cables for larger bins. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Pod bus | RS-485 with a small microcontroller in each pod. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Power and fan interface | Solar 12 V controller with an electrician-installed interposing relay kit, rather than powering the controller from the fan starter. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Battery chemistry | AGM lead-acid rather than lithium iron phosphate, because it accepts charge below 0 °C. Decided by Amish, 2026-09-25: go with recommendation. (Capacity was O2, decided on 2026-10-02.) |
| D9 | Plenum sensing | Add a plenum sensor at TRL 3 if the budget allows, in place of a predicted fan heat rise. Decided by Amish, 2026-09-25: go with recommendation. At TRL 3 the lowest-cost form, a temperature-only probe in the fan transition, costs $9.50 and does not fit in $250 with the kit at $247.00 (GGD-CAL-001, section H), so it is carried as a priced option (BOM item 14). Whether to adopt it anyway is O3. |
| D10 | Headspace CO₂ sensor | Offer as an option, not in the base kit. Decided by Amish, 2026-09-25: go with recommendation. |
| D11 | First region and crop | Shelled corn in a small US Midwest bin for the first co-design. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Items left open by this record (O3 decided in GGD-DDR-002; O1 and O2 decided on 2026-10-02).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First host farm and electrician for a co-design visit | **Decided by Amish, 2026-10-02:** recruit the host farm and its electrician through a land-grant extension grain-storage specialist, for example at Purdue University or Iowa State University, choosing a farm with a small corn bin, an aeration fan and a center hanger; the route to a first candidate, not an agreed partner (GGD-DEC-001, item 4). |
| O2 | Battery and panel capacity for R8 | **Decided by Amish, 2026-10-02:** a 20 W panel, provided the mast check with the stay removed is rerun for the larger panel and still passes (GGD-DEC-001, item 2). At TRL 3 a 3 mA relay input meets the autonomy half of R8 at no cost, but the 3-day recovery half needs a panel of about 19 W (GGD-CAL-001, section D). |
| O3 | Adopt the plenum probe despite the budget | Decided by Amish, 2026-09-25: go with recommendation (GGD-DDR-002). It removes the largest decision error (about 1 point of EMC per °C of fan heat) for $9.50 and would put the kit at $256.50, 2.6 % over $250. Recommendation: adopt it and accept the $6.50 overrun, since no other $9.50 buys as much decision accuracy. The probe is now BOM item 14 in the base kit, and the kit is $256.50. |

## Consequences

- `project.yaml`: `budget_usd` stays $250 and the pitch is reworded as in D2. `README.md` matches.
- GGD-PRB-001, GGD-PRC-001 and GGD-REQ-001 are revised to v0.3. R13 is redefined per bin with the receiver per farm (D1). R4 names the plenum-air EMC as calculated from the ambient humidity ratio and the fan heat, measured when the probe option is fitted. The key design choices in the precis are no longer "proposed".
- The BOM carries the D1 trims: pods 2a (SHT45, two) and 2b (SHT40, four), a 280 x 230 x 130 mm enclosure at $12, and 16 m of bus cable. The per-bin kit is $247.00 (GGD-CAL-001, H1).
