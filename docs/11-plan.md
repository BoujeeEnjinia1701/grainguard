---
doc_id: GGD-PLN-001
title: GrainGuard project plan
project: GrainGuard
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.8 upgrade, stage P3)
---

# GrainGuard project plan

GrainGuard is at stage P3 (design outputs) and TRL 3, the portfolio's caps. The next gate, P4 verification at TRL 4, is on hold until Amish lifts the cap. Three decisions are requested now: the concept choice (GGD-DEC-001 open item 10: all three options within 10 %, option A the design of record), the battery's disconnect setting against cold (open item 11, recommended: the battery maker's 65 % figure) and, when the cap lifts, the first contact with a land-grant extension grain-storage specialist to find the host farm. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Pipeline documents | Project lead | STM, OPT, URS, PRS, RTM, REG, FEA, RSK, MKT, PLN | Done at P3 (this session) |
| Design and calculations | Design lead | GGD-PRC-001, GGD-CAL-001, the D3 model of every option, STEP and STL, drawings GGD-DWG-001 and 101 to 111 | Done at P3; open items 10 and 11 with Amish |
| Build plan | Design lead | GGD-BLD-001 with pictures from the model | Done at P3 |
| Renders and storefront images | Project lead | Options picture, product renders, cards (on Amish's Mac) | Waiting for the next render session |
| Co-design partner | Project lead | A host farm with a small corn bin, a rated center hanger and an electrician, through an extension specialist | On hold (TRL 4 work) |
| Verification | Design lead | Bench and field tests of P4 | On hold (cap) |

## Resources needed

Table 2. Resources (P4 and later are planned, not started; costs are estimates).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Parts for one prototype and its receiver | A built kit to the build plan | One farm workshop, about two weeks | 432.50 (BOM, indicative) |
| Local fabricator | The mast weldment | Half a day | To quote locally |
| Licensed electrician | The relay kit at the host farm's starter | Half a day | To quote locally |
| Extension grain-storage specialist | Review of the control rule and targets; host farm | A few hours of meetings | None expected (extension service) |
| Laboratory or meter moisture samples | The PR-002 comparison | One season of sampling | To assess |
| Hazardous-locations reviewer | Assessment of the pods and cable in a dusty bin (GGD-REG-001 A2) | A review | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Met |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT, REG complete | Met |
| P2 Design inputs | PRS with targets, tolerances and verification, CAL, RTM, concept selection DDR (GGD-DDR-004, awaiting Amish), STEM check (open: S17 with Amish, seven rows to measure) | Met on paper; concept choice open |
| P3 Design outputs | D3 model, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability | Met (this session) |
| P4 Verification | Bench tests (relay fail-off, power budget, probe check), coated test board through a fumigation, moisture comparison, radio survey | On hold (cap) |
| P5 Validation | A season on the host farm with the farmer and the extension specialist | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish decides GGD-DEC-001 open item 10 (concept choice; no pick, all within 10 %) and open item 11 (disconnect setting; recommended the 65 % figure).
2. On Amish's Mac: the options picture (`python .kit/options.py`) and the product renders from `cad/src/product_model.py`.
3. When the cap lifts: contact a land-grant extension grain-storage specialist (GGD-DEC-001, item 4 of 2026-10-02), then the TRL 4 tests in the order of the build plan's first checks.

## References

Every source cited in this repo's documents, Chicago style.

- Analog Devices. "DS18B20 Programmable Resolution 1-Wire Digital Thermometer." https://www.analog.com/en/products/ds18b20.html.
- ASABE. *D245.6: Moisture Relationships of Plant-Based Agricultural Products*. St. Joseph, MI: ASABE.
- ASABE. *D272: Resistance to Airflow of Grains, Seeds, Other Agricultural Products, and Perforated Metal Sheets*. St. Joseph, MI: ASABE.
- Battery Design. "IEC 62485-2." https://www.batterydesign.net/legislation-rules-and-regulations/iec-62485-2/. Accessed 2026-10-24.
- Country Guide. "Options for Monitoring Grain Bins." https://www.country-guide.ca/crops/options-for-monitoring-grain-bins/. Checked 2026-09-25.
- EC&M. "NEC Article 502 Summary." February 6, 2024. https://www.ecmweb.com/national-electrical-code/article/21281848/nec-article-502-summary. Accessed 2026-10-24.
- FAO. *Manual of Fumigation for Insect Control*. https://www.fao.org/4/x5042e/x5042e0a.htm.
- Farm Progress. "Grain Temp Monitoring Not Out of Reach." July 15, 2020. https://www.farmprogress.com/farming-equipment/grain-temp-monitoring-not-out-of-reach. Accessed 2026-10-24.
- Feed and Grain. "Purdue Annual Study Reports Drop in Confined Space Incidents in 2023." https://www.feedandgrain.com/safety/worker-safety/article/15704874/purdue-annual-study-reports-drop-in-confined-space-incidents-in-2023.
- Forum News Service. "South Dakota Farmer Builds Bin Control for $100 Instead of $80K." *Brainerd Dispatch*, 2021. https://www.brainerddispatch.com/business/south-dakota-farmer-builds-bin-control-for-100-instead-of-80k. Accessed 2026-10-24.
- Grain Bin Monitoring System. GitHub. https://github.com/RonTCC/Grain-Bin-Monitoring-System.
- Hackaday.io. "Bin Temperature Monitoring System." https://hackaday.io/project/166702-bin-temperature-monitoring-system.
- Ileleji, K. E., et al. Hot spot detection in stored grain. *Applied Engineering in Agriculture* 22, no. 2. Purdue University. https://engineering.purdue.edu/ABE/people/Papers/klein.ileleji.1/hotspot.
- Illinois Experts. "Forces on Monitoring Cables during Grain Bin Filling and Emptying." ASABE. https://experts.illinois.edu/en/publications/forces-on-monitoring-cables-during-grain-bin-filling-and-emptying/.
- INOTEC. "Venting and Aerating Batteries." https://www.inotec-licht.de/en/practice/venting-and-aerating-batteries/. Accessed 2026-10-24.
- Kumar, Deepak, and Prasanta Kalita. "Reducing Postharvest Losses during Storage of Grain Crops to Strengthen Food Security in Developing Countries." *Foods* 6, no. 1 (2017). https://pmc.ncbi.nlm.nih.gov/articles/PMC5296677/.
- Legal Information Institute. "29 CFR 1910.272, Grain Handling Facilities." https://www.law.cornell.edu/cfr/text/29/1910.272. Accessed 2026-10-24.
- Legal Information Institute. "47 CFR 15.247, Operation within the Bands 902 to 928 MHz, 2400 to 2483.5 MHz, and 5725 to 5850 MHz." https://www.law.cornell.edu/cfr/text/47/15.247. Accessed 2026-10-24.
- Oklahoma State University Extension. "Aeration Management: Knowing When to Run Aeration Fans." BAE-1116. https://extension.okstate.edu/fact-sheets/aeration-management-knowing-when-to-run-aeration-fans.html.
- Parker Steel. "Declaration of Performance, S195T Gas and Water Tube to EN 10255." https://parkersteel.co.uk/webshared/media/pdf/dop/PS-DOP028-S195T-GAS-WATER.pdf. Accessed 2026-10-24.
- Sensirion. "SHT40." https://sensirion.com/products/catalog/SHT40; "SHT45." https://sensirion.com/products/catalog/SHT45; "SHT4x Datasheet." https://sensirion.com/resource/datasheet/sht4x.
- Trojan Battery. *Deep Cycle Battery Storage Guide* (freezing points after the BCI *Battery Service Manual*, 1995). https://ressupply.com/documents/trojan_battery/Deep_Cycle_Battery_Storage_Guide.pdf. Accessed 2026-10-24.
- University of Minnesota Extension. "Managing Stored Grain with Aeration." https://extension.umn.edu/corn-harvest/managing-stored-grain-aeration.
- USDA Agricultural Research Service. "Accuracy of Grain Moisture Content Prediction Using Temperature and Relative Humidity Sensors." https://www.ars.usda.gov/ARSUserFiles/30200525/362AccuracyGrainMoistureContentPrediction.pdf.
- World Grain. "Early Spoilage Detection." https://world-grain.com/articles/10162-early-spoilage-detection. Accessed 2026-10-24.
