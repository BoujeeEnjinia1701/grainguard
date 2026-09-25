---
doc_id: GGD-PRB-001
title: GrainGuard problem statement
project: GrainGuard
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 decisions (GGD-DDR-001); reference case corrected to 88.8 t; budget per bin with the receiver per farm; open questions updated
---

# GrainGuard problem statement

Stored grain spoils when bins are aerated at the wrong times: fans run in humid air rewet the grain, fans left off let warm spots grow, and on many small farms the only tools are a manual switch, a thermostat and a person climbing the bin to check it. GrainGuard aims to give an existing bin a low-cost sensor cable and a fan controller that decides from measured air and grain conditions when running the fan helps.

## The problem

Grain goes into storage warm and often near its upper safe moisture. Aeration fans push outside air through the grain to cool it and keep it uniform. Extension guidance is clear on the principle: run fans when outside air is cooler than the grain, and remember that the moisture the grain ends at is set by the temperature and relative humidity (RH) of the air, not by fan size ([Oklahoma State University, BAE-1116](https://extension.okstate.edu/fact-sheets/aeration-management-knowing-when-to-run-aeration-fans.html)). The balance point is the equilibrium moisture content (EMC) of the air. If the EMC of the air entering the bin is above the grain's moisture, the fan adds water; if it is below, the fan dries.

Getting this right by hand is hard:

1. **Fall air is often humid.** At 10 °C and 70 % RH the EMC of shelled corn is about 15.7 % wet basis (estimate from the ASABE D245.6 modified Henderson equation), so a fan running then slowly rewets corn stored at 15 %. The same air warmed 1 °C by the fan drops to about 14.7 %, which dries it slightly. The difference is too fine to judge by eye.
2. **Fans take days to finish a job.** At an airflow of about 0.08 m³/min per m³ of grain (0.1 cfm/bu), a cooling front needs 100 to 200 h of fan time to pass through a bin ([University of Minnesota Extension](https://extension.umn.edu/corn-harvest/managing-stored-grain-aeration)), so the farmer must track fan hours across many days and weather changes.
3. **Trouble starts where no one can see it.** Spoilage often begins at the center core of fines or at the top surface. A temperature sensor must be within about 0.5 m of a developing hot spot to see it ([Ileleji et al., Applied Engineering in Agriculture 22(2), Purdue](https://engineering.purdue.edu/ABE/people/Papers/klein.ileleji.1/hotspot)), and farmers who lack sensors must climb the bin to probe it.
4. **Checking bins is dangerous.** Grain entrapment was the leading cause of agricultural confined-space incidents in the United States in 2023: 27 of 55 cases, and 59 % of those entrapments were fatal ([Purdue 2023 summary, reported by Feed and Grain](https://www.feedandgrain.com/safety/worker-safety/article/15704874/purdue-annual-study-reports-drop-in-confined-space-incidents-in-2023)). Every avoided trip into or onto a bin removes exposure.

Commercial monitoring and fan control exists but is priced for large sites. One self-install kit with fan controller and CO₂ sensor was reported at about US$3,000 per bin ([Country Guide](https://www.country-guide.ca/crops/options-for-monitoring-grain-bins/)). Open hobbyist projects exist but monitor temperature only and do not control fans; one uses three DS18B20 sensors per cable and reports about CA$500 in parts for four bins ([Bin Temperature Monitoring System, Hackaday.io](https://hackaday.io/project/166702-bin-temperature-monitoring-system); see also [Grain Bin Monitoring System, GitHub](https://github.com/RonTCC/Grain-Bin-Monitoring-System)).

The stakes are higher where storage is poorer. Reviews report storage losses of cereals of 20 % to 40 % in parts of sub-Saharan Africa and far lower losses where storage is managed with modern methods ([Kumar and Kalita, Foods 6(1), 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5296677/)). GrainGuard does not address hermetic or bag storage, but a low-cost aerated bin controller could later serve cooperatives with small steel silos and fans.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Small or mid-size grain farmer | Know grain temperature and moisture without climbing the bin; have fans run only when they help | 1 to 10 corrugated steel bins of 4.5 to 9 m (15 to 30 ft) diameter with existing aeration fans and manual or thermostat control |
| Farm worker or family member | Fewer trips up the bin ladder and no need to enter a bin to check grain | Harvest and winter holding, often in cold and dark |
| Farm electrician | A small, clearly isolated interface to an existing fan starter | Existing single-phase or three-phase fan motor of about 0.75 to 2.2 kW (1 to 3 hp) |
| Cooperative or storage manager (later) | A low-cost, repairable monitor for small steel silos | Emerging markets with aerated storage; out of scope for the first prototype |
| Open hardware community | A documented design to build, audit and adapt | Makerspaces, extension programs, agricultural engineering courses |

**Reference case.** A 5.49 m (18 ft) diameter bin with a 5.6 m eave, a full perforated floor 0.4 m above the pad and one existing aeration fan, filled level to the eave with shelled corn: 5.2 m of grain, about 123 m³, 3,493 bu or 88.8 t (GGD-CAL-001). The first region and crop are corn in a small US Midwest bin (GGD-DDR-001, D11).

## Constraints

- Garage-buildable prototype, $250 USD or less in parts per bin, with the farmhouse receiver costed once per farm (see GGD-REQ-001 R13 and GGD-DDR-001 D1).
- Retrofit to existing bins and fans with no welding or cutting of bin sheets and no change to the fan motor.
- Installation and service without entering a bin that contains grain.
- No mains voltage inside the GrainGuard controller; the only mains-connected item is a small relay kit installed by a licensed electrician in or beside the existing fan starter.
- Works through a northern winter (-30 °C) and a hot, dusty summer; many bins have no mains outlet nearby, so the controller runs on solar power.
- Data stays on the farm by default.

## Out of scope

- Natural-air or heated-air drying of wet grain at high airflow. GrainGuard controls aeration for cooling and holding, with a gentle drying bias; full in-bin drying control is a later extension.
- Hermetic storage, bags and granaries without fans.
- Fumigation control and phosphine monitoring.
- Grain level or inventory measurement.
- Cloud services.

## Open questions

- First region and crop: decided as corn in a small US Midwest bin (GGD-DDR-001, D11; decided by Amish, 2026-09-25).
- Headspace CO₂ sensor: decided as an option, not in the base kit (GGD-DDR-001, D10; decided by Amish, 2026-09-25).
- Which farm and electrician would host a first co-design visit? Proposed, awaiting Amish (GGD-DDR-001, O1); partners are to be picked per area later.
