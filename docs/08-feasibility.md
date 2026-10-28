---
doc_id: GGD-FEA-001
title: GrainGuard feasibility assessment
project: GrainGuard
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.8 upgrade)
---

# GrainGuard feasibility assessment

GrainGuard is feasible on paper: the physics is sound and every part can be bought or made in a farm workshop, but two things only a trial can settle (whether interstitial RH predicts moisture to ±0.8 points, and what a thin cable really pulls on a bin's roof hanger) and one decision for Amish (the battery's disconnect setting against cold, GGD-DEC-001 open item 11) stand between it and a working prototype. Cost is the weakest aspect: USD 410.50 per bin against a USD 260 value-engineering target. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | The working principle is within known science (22 of 30 claims within, 7 plausible to confirm by measurement, 1 fix proposed); the decision rule's key input, the fan heat, is measured by the plenum probe; the D3 model of all 331 parts passes the fidelity and interference checks | High | Moisture estimate at risk (PR-002); a center cable watches 3.3 % of the cross-section (PR-006) | GGD-STM-001; GGD-CAL-001 B, C; `cad/fidelity.json` |
| Materials | Galvanized and stainless steel, aluminium sheet and angle, printed ASA, polycarbonate box; all common. ASA pods and coated boards face grain dust and phosphine | Medium | Phosphine resistance of the coated boards unverified (S28); ASA outdoors and in grain to confirm | GGD-STM-001 S28; BOM lines 2, 4, 9 |
| Manufacturing and assembly | Cutting, drilling and bending angle and sheet, one small weldment (or a local fabricator), 3D printing and screw-terminal wiring; the build plan covers every part in order, and the D3 model fixed five fit details (D11) | High | Roof work and an empty-bin entry to fit the cable need a confined-space procedure and fall protection | GGD-BLD-001; GGD-DEC-001 D11 |
| Power and controls | 3.28 Wh per day; 7.7 days with no sun; 20 W panel refills in 2.9 winter days with the mast south of the bin (D13); fail-off relay, timeout and hand position | Medium | Thin refill margin (2.9 against 3 days); the battery's freezing point needs a higher disconnect setting, which cuts autonomy to 5.4 days (open item 11) | GGD-CAL-001 D, G; STEM check S13, S14, S17 |
| Radio | 16.9 dB margin at 1 km past one building; 24-byte packets within the 0.4 s dwell limit | High | Real farms add more obstructions; a site survey at TRL 4 | GGD-CAL-001 E; GGD-REG-001 R1 |
| Structure | Mast 2.7 times below yield with the stay; 1.7 times with the stay off in gusts under 30 m/s (D12); rope 4.3 times the largest force measured on any cable | Medium | Roof hanger rating per bin (PR-010); anchor capacity to confirm with the anchor maker (S26) | GGD-CAL-001 F |
| Supply of parts | Every line is a common retail item (sensors, LoRa module, AGM battery, PWM controller, 20 W panel, glands, galvanized pipe and angle); no single supplier needed | High | Prices are indicative, not quotes; the adjustable-disconnect controller and the labyrinth vents are estimates | `bom/bom.csv`; GGD-MKT-001 |
| Cost | USD 410.50 per bin, USD 150.50 over the USD 260 value-engineering target; commercial cables and fan control cost several times more per bin | Low | The mast, pods and relay kit drive the cost; savings in GGD-DEC-001 (Value engineering) and the option C graft in GGD-OPT-001 | GGD-CAL-001 H; GGD-DEC-001 |
| Regulatory | Radio and battery ventilation met by design; the hazardous-location status of the pods inside a dusty bin is unassessed | Medium | To assess with a reviewer before any product claim | GGD-REG-001 A2 |

Ratings: High, Medium, Low.
