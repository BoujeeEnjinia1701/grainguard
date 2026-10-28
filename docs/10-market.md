---
doc_id: GGD-MKT-001
title: GrainGuard market and viability
project: GrainGuard
doc_type: Market and viability
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

# GrainGuard market and viability

GrainGuard is for small and mid-size farms with a few aerated steel bins, who now choose between a manual switch, a thermostat and commercial monitoring and fan control quoted at USD 1,000 to 8,000 per bin. An open design at about USD 410 per bin, buildable and repairable on the farm, sits between a farmer's own smart-switch hack (which watches only the weather) and the commercial systems, and it is the only one of the three that is documented for anyone to audit and adapt. Prices are cited with the date they were checked; GrainGuard's own cost is the indicative BOM, not a quote. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Small and mid-size grain farms with aerated steel bins | Farms with 1 to 10 bins of 4.5 to 9 m, US Midwest first (GGD-DDR-001, D11) | A self-install monitoring kit with fan controller and CO₂ sensor at about USD 3,000 per bin (Country Guide); temperature cables at USD 275 to 300 each, a handheld reader at USD 500 and remote monitoring adding USD 3,500 to 4,000 (Farm Progress, 2020); automated bin control quoted to one farmer at about USD 8,000 per bin, with vendors suggesting about USD 1,000 per bin (Forum News Service, 2021) | 410.50 per bin plus 22.00 per farm for the receiver (BOM) | Grain temperature profile, moisture estimate and fan control that runs only when the air helps, for a fraction of a commercial system; no subscription; data stays on the farm |
| Farmers who build their own | The same farms, with a farmer handy with electronics | A farmer-built system of a Wi-Fi temperature and humidity controller (about USD 24) and smart switches (about USD 6 each), about USD 100 for 10 bins, switching fans on outside air only (Forum News Service, 2021); an open temperature-only cable project at about CA$500 in parts for four bins (Hackaday.io) | 410.50 per bin (option A); about 170 for the weather-only option C (GGD-OPT-001, estimate) | A documented, safety-reviewed design with grain sensing and a fail-off relay installed by an electrician, rather than a consumer switch in a mains starter |
| Cooperatives with small steel silos (later) | Emerging markets with aerated storage, where cereal storage losses reach 20 % to 40 % (Kumar and Kalita, 2017) | Commercial systems as above, rarely sold there | To estimate locally (868 MHz radio, local parts) | Repairable monitoring and control with local parts; out of scope for the first prototype |
| Extension programs and agricultural engineering courses | Land-grant universities, makerspaces | None open with fan control found | 410.50 per teaching kit | A complete open reference design with calculations, drawings and a build plan |

## Open route

The first builder is a farm workshop with a local fabricator for the mast weldment and a licensed electrician for the relay kit; the parts are retail items with no single supplier. The design spreads through land-grant extension programs (the route to the first host farm, GGD-DEC-001 item 4 of 2026-10-02), makerspaces and agricultural engineering courses, which can build it as a teaching kit and feed back data from real bins. It stays open under CERN-OHL-S-2.0 for the hardware and MIT for the software, so any improvement to a built kit stays shareable. Volume would come from buying cable, clamps and fixings for several bins at once, which lowers lines 3, 10 and 13 per bin (GGD-DEC-001, Value engineering). A commercial version would need the hazardous-location assessment, radio module certification and a listed relay panel (GGD-REG-001).

## Sources

- Country Guide, "Options for monitoring grain bins," https://www.country-guide.ca/crops/options-for-monitoring-grain-bins/, as cited in GGD-PRB-001 (checked 2026-09-25; the page could not be reached from this session on 2026-10-24) (about USD 3,000 per bin for a self-install kit with fan controller and CO₂ sensor).
- Farm Progress, "Grain temp monitoring not out of reach," 15 July 2020, https://www.farmprogress.com/farming-equipment/grain-temp-monitoring-not-out-of-reach, accessed 2026-10-24 (cables USD 275 to 300; handheld reader USD 500; remote monitoring adds USD 3,500 to 4,000).
- Forum News Service, "South Dakota farmer builds bin control for $100 instead of $80K," Brainerd Dispatch (2021; date inferred from the article's photos), https://www.brainerddispatch.com/business/south-dakota-farmer-builds-bin-control-for-100-instead-of-80k, accessed 2026-10-24 (about USD 8,000 per bin quoted; vendors about USD 1,000 per bin; farmer-built system about USD 100 for 10 bins).
- Bin Temperature Monitoring System, Hackaday.io, https://hackaday.io/project/166702-bin-temperature-monitoring-system, as cited in GGD-PRB-001 (checked 2026-09-25) (about CA$500 in parts for four bins, temperature only).
- D. Kumar and P. Kalita, "Reducing Postharvest Losses during Storage of Grain Crops to Strengthen Food Security in Developing Countries," *Foods* 6, no. 1 (2017), https://pmc.ncbi.nlm.nih.gov/articles/PMC5296677/, as cited in GGD-PRB-001 (checked 2026-09-25).
- GrainGuard bill of materials, `bom/bom.csv` (indicative retail prices for one prototype in 2026, not quotes).
