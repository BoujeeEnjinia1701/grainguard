---
doc_id: GGD-DDR-004
title: GrainGuard concept selection
project: GrainGuard
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: Concept selection between options A, B and C of GGD-OPT-001; all within 10 %, sent to Amish without a pick
---

# 0004: Concept selection

- **Date:** 2026-10-24
- **Status:** proposed, awaiting Amish. No option is recommended: the three weighted scores are within 10 % (STANDARDS section 21). Option A stays the design of record until Amish decides.

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements, with the current design of a repo designed before kit 1.8 as option A (STANDARDS section 21). GrainGuard reached TRL 3 on option A, a sensor cable down the bin axis with a solar controller on a mast. The kit 1.8 upgrade of 2026-10-24 added two options with different principles (GGD-OPT-001), modelled each at detail level D3 (kit 1.9, `cad/src/model.py`), checked their science (GGD-STM-001, rows B1 to C3) and scored all three against the seventeen user requirements of GGD-URS-001 plus cost, buildability, safety and maintenance.

## Options considered

| Option | Working principle | Score (of 245) | Estimated cost per bin | What it gives up |
| --- | --- | --- | --- | --- |
| A, center sensor cable with EMC fan control | Six T and RH pods on a rope read the grain; plenum-EMC fan rule; solar controller on a mast | 193 | USD 410.50 (priced BOM) | Cost (USD 150.50 over the target), empty-bin installation, roof load during unloading |
| B, headspace sensor head with CO₂ watch | A head under the peak reads the air leaving the grain and its CO₂; wall-mounted solar controller | 186 | About USD 370 (estimate) | The temperature profile (PR-001) and per-level moisture (PR-002) |
| C, fan-side weather controller | Outside-air EMC and a cooling-front model; powered from the relay kit | 192 | About USD 170 (estimate) | Every grain measurement: PR-001, PR-002 and PR-006 |

## Decision

None yet. The options are within 10 % (B is 3.6 % below A, C 0.5 % below A), so all three go to Amish without a pick, recorded as open item 10 in GGD-DEC-001.

For his decision: option A is the only option that meets PR-001, PR-002 and, near the center, PR-006, the requirements behind the pitch. Options B and C would change the pitch and what GrainGuard is, which is his decision in any case. Whatever he picks, two ideas from the runners-up are worth grafting onto option A: powering the controller from the relay kit's 24 V supply where the starter is near (from C; removes the panel, battery and charge controller, USD 76, and the battery's cold and hydrogen issues), and the headspace CO₂ head as a priced option on the same shackle (from B; widens heating detection beyond the center core).

## Consequences

- If Amish keeps option A, nothing in the design changes; `concept_chosen` becomes A and the two grafts can be put to him as separate decisions.
- If he picks B or C, the pitch, the PRS (PR-001, PR-002 and PR-006 would be restated or withdrawn), the BOM, the build plan, the drawings and the calculation note are redone for that option at the next session; the D3 models of B and C in `cad/src/ggd_options.py` are the starting point.
- `project.yaml` keeps `concept_chosen: A (proposed)` until he decides.
