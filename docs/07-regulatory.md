---
doc_id: GGD-REG-001
title: GrainGuard regulatory and standards register
project: GrainGuard
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.8 upgrade); United States as the first jurisdiction (GGD-DDR-001, D11)
---

# GrainGuard regulatory and standards register

Which standards and regulations would apply to GrainGuard as a product, where, and what is needed. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. The first region is a small corn bin in the US Midwest (GGD-DDR-001, D11), so the rows are United States rules unless stated. Three rows shape the design now: the radio rule (the payload is held to 24 bytes so a packet stays under the 0.4 s dwell limit), battery ventilation (the two labyrinth vents of GGD-DEC-001 D10) and the hazardous-location question for the pods inside a dusty bin, which is the largest regulatory unknown. No certification is pursued while the portfolio is capped at TRL 3. This is the first register in the agriculture focus area, so rows A1 to A3 are the shared research for other agriculture repos to cite. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | OSHA 29 CFR 1910.272, grain handling facilities | United States | Grain dust fire and explosion control and bin entry: lockout of equipment, body harness and lifeline, an observer outside | Appendix A says it does not apply to on-farm storage, but its bin-entry practice is what the build plan's safety stops follow (GGD-BLD-001, S2) | Project lead | Does not apply (on-farm); practice followed |
| A2 | NFPA 70 (National Electrical Code), Articles 500 and 502, Class II locations (combustible dust) | United States, as adopted by states | Electrical equipment where combustible dust is present | Grain dust in the headspace makes the bin's interior a candidate Class II location; the pods and bus cable are inside it at 12 V and a few milliamps, but no hazardous-location assessment has been made (STEM check S29) | Electronics lead with a hazardous-locations reviewer | To assess |
| A3 | NFPA 70, the local electrical code for the starter and wiring outside the bin | United States, as adopted by states | Wiring methods and equipment at the fan starter | The relay kit is the only mains item and is installed by a licensed electrician to the local code (PR-012) | Licensed electrician | Applies (installer's responsibility) |
| R1 | 47 CFR 15.247, operation in 902 to 928 MHz | United States | Frequency hopping with hopping channels under 250 kHz wide: at least 50 channels and no more than 0.4 s on any channel in 20 s; 1 W | The LoRa link (125 kHz channels) keeps each 24-byte packet at 371 ms (GGD-CAL-001 E5, PR-007); use a radio module already certified for the band | Electronics lead | Met by design (module certification needed for any product) |
| R2 | EU Radio Equipment Directive 2014/53/EU (868 MHz variant) | European Union | Radio and EMC conformity | Only if an 868 MHz variant is made outside the Americas | Electronics lead | Does not apply now |
| R3 | IEC 60529, degrees of protection provided by enclosures (IP code) | International | Dust and water ingress ratings | Controller box IP66 (bought rating) with two labyrinth vents of IP55 or better (D10); pods dust-tight with a membrane (PR-009) | Design lead | Met by design (bought ratings), to verify after drilling at TRL 4 |
| R4 | IEC 62485-2 (formerly EN 50272-2), safety requirements for secondary batteries and battery installations, stationary batteries | International | Ventilation of battery spaces against hydrogen: Q = 0.05 n Igas C 10⁻³ m³/h, opening A = 28 Q cm² | The 7 Ah AGM battery in a closed box: two vents of 0.79 cm² each against 0.47 cm² needed (GGD-CAL-001 G4) | Design lead | Met by design (method followed; conformance not claimed) |
| R5 | UL 508A, industrial control panels | United States | Construction and listing of control panels | The relay kit's box (BOM line 11) if sold as a product; the prototype uses listed components installed by an electrician | Electronics lead | To assess (product stage) |
| R6 | 49 CFR 173.159a, non-spillable lead-acid batteries in transport | United States | Shipping of sealed lead-acid batteries | The AGM battery if kits are shipped with it | Procurement | To assess (product stage) |
| R7 | Phosphine fumigant labels under FIFRA (US EPA) | United States | Use, aeration and re-entry rules for phosphine, binding on the certified applicator | GrainGuard does not measure phosphine and must never be used to judge whether a bin is safe to enter (GGD-PRC-001, Safety) | Licensed fumigator | Does not apply to the device; design note |
| R8 | ASABE D245.6 (moisture relationships) and D272 (resistance to airflow) | International (engineering data) | Equilibrium moisture and airflow resistance data for grains | The EMC equation and static pressure in GGD-CAL-001 | Design lead | Applies (reference data) |
| R9 | EU RoHS Directive 2011/65/EU and WEEE Directive 2012/19/EU | European Union | Hazardous substances and take-back of electrical equipment | Boards and the battery, only if sold in the EU | Electronics lead | Does not apply now |

Status: to assess, applies, does not apply, met by design, certification needed later.

Options B and C (GGD-OPT-001) share rows R1, R3, R5 and R7. Option B moves the electronics in the bin to a head in the headspace, where A2 applies in the same way, and keeps the battery (R4, R6). Option C has nothing in the bin and no battery, so A2, R4 and R6 drop out, but it takes its power from the relay kit's supply, which puts more of it under A3 and R5.

## Sources

- OSHA 29 CFR 1910.272, Grain handling facilities, including Appendix A, Legal Information Institute, https://www.law.cornell.edu/cfr/text/29/1910.272, accessed 2026-10-24.
- 47 CFR 15.247, Operation within the bands 902 to 928 MHz, 2400 to 2483.5 MHz and 5725 to 5850 MHz, Legal Information Institute, https://www.law.cornell.edu/cfr/text/47/15.247, accessed 2026-10-24.
- EC&M, "NEC Article 502 summary," 6 February 2024, https://www.ecmweb.com/national-electrical-code/article/21281848/nec-article-502-summary, accessed 2026-10-24.
- Battery Design, "IEC 62485-2," https://www.batterydesign.net/legislation-rules-and-regulations/iec-62485-2/, and INOTEC, "Venting and aerating batteries" (EN 50272-2 formula), https://www.inotec-licht.de/en/practice/venting-and-aerating-batteries/, accessed 2026-10-24.
- Rows A3, R2, R3, R5, R6, R7, R8 and R9 are listed from the standards' and laws' own titles; their applicability is "to assess" or a design note and needs a test laboratory, an electrician or a regulatory consultant before any product claim.
