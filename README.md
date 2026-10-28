# GrainGuard

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827) [![DOI](https://zenodo.org/badge/1386351914.svg)](https://zenodo.org/badge/latestdoi/1386351914) [![REUSE compliant](https://github.com/BoujeeEnjinia1701/grainguard/actions/workflows/reuse.yml/badge.svg)](https://github.com/BoujeeEnjinia1701/grainguard/actions/workflows/reuse.yml) [![Archived in Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/BoujeeEnjinia1701/grainguard/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/BoujeeEnjinia1701/grainguard)

**Area:** Agriculture · **TRL:** 3 of 9 (proof of concept on paper) · **Value-engineering target:** USD 260 per bin (estimated cost of the constructable design USD 410.50) · **Difficulty:** 2 of 5

Cable of moisture and temperature probes strung through the bin, plus a controller that runs aeration fans only when the air will cool or dry the grain.

![GrainGuard: grain bin sensor cable and aeration fan controller, product render](media/render-hero.png)

[Exploded render](media/render-exploded.png) · [Detail render](media/render-detail.png) · [Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement GGD-DWG-001 (PDF)](cad/drawings/GGD-DWG-001.pdf) · [STEM check GGD-STM-001](docs/01b-stem-check.md) · [Concept options GGD-OPT-001](docs/02a-concept-options.md) · [User requirements](docs/03a-user-requirements.md) · [Product requirements](docs/03-requirements.md) · [Traceability](docs/03b-traceability.md) · [Sizing note GGD-CAL-001](docs/04-calcs/01-sizing.md) · [Prototype build plan](docs/05-build-plan.md) · [Decisions](docs/06-design-decisions.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Most spoilage in an aerated bin starts with a fan run at the wrong time or a warm spot nobody saw, and both problems come down to measurement. A farmer standing beside a bin cannot tell whether a given hour's air will dry the grain or wet it, and cannot see a hot spot forming 3 m inside the grain. GrainGuard puts cheap, well-characterized temperature and humidity sensors where the answers are (in the grain, in the outside air and in the fan's discharge) and lets a small controller apply the rule that extension services already publish. It retrofits an existing bin and fan rather than replacing them, keeps mains voltage out of its own box, and needs no one to enter a bin that holds grain.

It is open and garage-buildable because the farms that most need it are the ones commercial systems price out. The parts are off-the-shelf sensors, a LoRa board, a small solar kit and a relay kit that any farm electrician can wire, so a farmer, an extension program or a cooperative can build, repair and adapt it, change the crop constants for local grain, and audit exactly how the fan decision is made.

## Burning platform

The FAO estimates that [13.3 % of the world's food was lost after harvest in 2023](https://www.fao.org/sustainable-development-goals-data-portal/data/indicators/1231-global-food-losses/en/), before it reached retail, on farms and in transport, storage, wholesale and processing. Poor storage costs more than grain: in 2004, maize stored damp in eastern and central Kenya became contaminated with aflatoxin, and [by July 20 that year 317 cases of acute aflatoxicosis and 125 deaths had been reported](https://www.cdc.gov/mmwr/preview/mmwrhtml/mm5334a4.htm) (CDC, MMWR).

Spoiled grain also kills the people who try to fix it. Grain that has crusted in storage and will not flow is one reason people enter bins, and in the United States [grain entrapments made up 34 of the 51 agricultural confined-space cases documented in 2024, with 41.2 % of entrapments fatal](https://www.purdue.edu/engineering/abe/agconfinespaces/wp-content/uploads/2025/05/2024-Summary-of-U.S.-Agricultural-Confined-Space-related-Injuries-and-Fatalities-Report.pdf) (Purdue University). Keeping grain in condition, and knowing its state without climbing the bin, removes both the loss and the reason to go in.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Row-crop farming | Aeration control and grain monitoring for on-farm corn, soybean and wheat bins |
| Grain cooperatives and country elevators | Low-cost monitoring of small satellite bins that do not justify a commercial cable system |
| Seed production | Holding seed lots cool and dry to protect germination |
| Livestock and feed milling | Condition monitoring of on-site feed grain bins |
| Agricultural extension and education | A transparent teaching kit for aeration management and grain drying courses |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | On-farm bins are common across the Corn Belt, and [grain entrapment is the leading cause of agricultural confined-space incidents](https://www.purdue.edu/engineering/abe/agconfinespaces/wp-content/uploads/2025/05/2024-Summary-of-U.S.-Agricultural-Confined-Space-related-Injuries-and-Fatalities-Report.pdf) |
| Australia | GRDC reports that [about two-thirds of Australian growers do not use aeration cooling](https://groundcover.grdc.com.au/farm-business/grain-storage/aeration-cooling-can-help-save-moist-grain), though it can be retrofitted to existing silos, and recommends an automatic controller |
| Brazil | Grain production outgrew storage by almost 90 Mt in 2021/22, and [only 15 % of farms have warehouses or silos](https://farmdocdaily.illinois.edu/2022/11/crop-production-in-brazil-outpaces-storage-capacity.html) (CONAB data), so new on-farm bins need affordable management |
| Kenya | Damp maize storage caused the [2004 aflatoxicosis outbreak](https://www.cdc.gov/mmwr/preview/mmwrhtml/mm5334a4.htm); cooperatives with small steel silos could use a low-cost condition monitor |
| India | A national study found [post-harvest losses of 3.89 % to 5.92 % for cereals](https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=1885038) (Ministry of Food Processing Industries, 2022), with storage one of the stages |

## What sparked the idea

The idea traces back to Mount Carroll, Illinois, in July 2010. Corn in a bin at Haasbach LLC was, in the words of an [NPR investigation](https://www.npr.org/transcripts/174828849), "wet and crusty, clogging the drain hole at the bottom and sticking to the walls", so workers were sent in to walk it down while the unloading equipment ran. Two teenagers, aged 14 and 19, were engulfed and killed, and OSHA later [cited the operator for willful violations](https://www.dol.gov/newsroom/releases/osha/osha20110124). The entry was a response to grain that had gone out of condition in storage. GrainGuard starts from the other end of that chain: measure the grain and the air, run the fan only when it helps, and see trouble early from the farmhouse, so that fewer bins ever reach the state that sends someone inside.

## Problem

Stored grain spoils when bins are aerated at the wrong times. Humid fall air can rewet grain, heating starts where no one can see it, and checking a bin by climbing it is dangerous. Commercial monitoring with fan control costs thousands of dollars per bin. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

One cable of six temperature and humidity pods hangs down the center of an existing bin. A solar-powered 12 V controller beside the bin compares the grain with the outside air, allows for the fan's own heat, and switches the existing fan through a small relay kit only when the air will cool or dry the grain. It reports to a farmhouse receiver by LoRa radio. TRL 3 calculations for an 18 ft (5.49 m) bin of about 88.8 t of corn: a sensor-induced moisture error of 0.23 to 0.42 points and 7.7 days of winter battery autonomy with no sun. Value-engineering target: USD 260 per bin. Estimated cost of the constructable design: USD 410.50 per bin (USD 150.50 over the target), with the farmhouse receiver costed per farm. The kit includes a USD 9.50 plenum probe that measures the fan's own heat ([GGD-DDR-002](docs/decisions/0002-recommendations-accepted.md)). Two requirements are not met on paper and have fixes with Amish: the 20 W panel refills the battery from half charge in 3.5 winter days, not 3, once the battery's charge efficiency is counted (a 25 W panel is proposed), and at the battery's 50 % disconnect setting its electrolyte could freeze at -30 °C (the 70 % figure is proposed); see [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## STEM check

Thirty-three claims for the design are checked ([GGD-STM-001](docs/01b-stem-check.md)): nineteen are within known science, twelve wait for measurements at TRL 4 or a purchase check (the moisture estimate, the probe and shield accuracy, the radio on a real farm, phosphine, grain dust and others), and two fail with a fix proposed to Amish (the battery's freezing point and the winter refill). Seven details failed along the way and were fixed under Amish's standing instruction: two vents let the battery's hydrogen out of the sealed box, the mast tube is checked at its real S195T grade with the stay taken off only in gusts under 30 m/s, the mast stands south of the bin so the bin never shades the panel, the radio uses a 500 kHz bandwidth (the legal mode in the US band), the plenum probe is zeroed against the outside-air sensor, and a 0.5 A fuse protects the thin bus cable inside the bin. An independent reviewer recomputed the results and its findings are recorded.

## Concept options

![Three ways to run a bin's aeration fan on measured air, side by side at one scale](media/options.png)

Three working principles are scored against the user requirements ([GGD-OPT-001](docs/02a-concept-options.md)): option A, the center sensor cable described here (193 of 245), option C, a fan-side weather controller with no sensor in the bin (192), and option B, a headspace sensor head with a CO₂ watch and no cable in the grain (186). They are within 10 % of each other, so the choice is with Amish without a pick, and option A stays the design of record; only option A measures the grain itself. All three are modelled at the same level of detail.

## Key components

- Six Sensirion SHT45 and SHT40 pods on a 6 mm steel wire rope, RS-485 bus
- LoRa controller in an IP66 box on a stayed steel mast, with its antenna
- Interposing relay kit with hand-off-auto switch, installed by an electrician at the fan starter
- Ambient temperature and humidity sensor in a radiation shield
- Plenum temperature probe in the fan transition, to measure the fan's own heat
- 20 W solar panel, charge controller and 12 V AGM battery
- Farmhouse LoRa receiver with display

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Building the prototype

The prototype build plan ([docs/05-build-plan.md](docs/05-build-plan.md)) shows how to make and fit every component, in order, with a making sketch for each made part, close-ups of the joints and a picture for every assembly step. Writing it made the design buildable: the pods became printed, openable bodies on rope stops, the mast a welded and stayed weldment, and every part on the mast got a clamp or bracket ([GGD-DDR-003](docs/decisions/0003-design-for-construction.md)). The work is metal cutting and drilling, one simple weldment, 3D printing and low-voltage wiring; the relay kit at the fan starter is fitted by a licensed electrician. Open decisions are kept in the [design decisions register](docs/06-design-decisions.md). The model in `cad/src/` draws every part, bolt, nut, washer, screw and weld of all three concept options (kit 1.9, detail level D3: 331 parts for option A), and STEP files of every made and bought part of option A are in `cad/step/A/`.

![GrainGuard prototype: every component, pulled apart and numbered in build order](docs/05-build-plan/overview.png)

## Safety

> **Safety:** Never enter a bin that holds grain. Install the cable only in an empty bin, with unloading equipment locked out, a confined-space procedure and a trained spotter. The fan starts automatically: lock out at the disconnect before touching it. Only a licensed electrician connects the relay kit to the fan starter. Hang the cable only from a roof hanger the bin maker rates for cable loads. See the safety section of [docs/02-concept.md](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, STEM check, concept and concept options, user and product requirements, traceability, calculations, build plan, decisions, regulatory, feasibility, risk, market and plan |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (GGD-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `GGD-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
